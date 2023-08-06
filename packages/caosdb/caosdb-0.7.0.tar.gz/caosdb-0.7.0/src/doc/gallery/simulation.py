"""
Run a simulation and store the values into CaosDB.

>>> main()              # doctest: +ELLIPSIS
These distances resulted in small x,y, values:
[...]
"""

import numpy as np
import scipy.integrate
import caosdb as db
from caosadvancedtools.table_converter import to_table


def setup_caosdb():
    """Create the data model and insert it into CaosDB

    The data model consists of the following RecordTypes:

    Software
      with author and revision.

    SoftwareRun
      A specific run of the sofware, with input parameters, time of completion and a result.

    State
      An aggregate of x,y,z values.

    Parameters
      In this case the x,y,z initial values before the integration, so this is just a state.

    Result
      The x,y,z values at the end of the software run, the final state.

    The data model of course also contains the corresponding properties for these RecordTypes.
    """

    cont = db.Container()  # Container to insert all Entities at once into CaosDB
    # create Properties
    cont.append(db.Property("x", datatype=db.DOUBLE))
    cont.append(db.Property("y", datatype=db.DOUBLE))
    cont.append(db.Property("z", datatype=db.DOUBLE))
    cont.append(db.Property("completed", datatype=db.DATETIME))
    cont.append(db.Property("author", datatype=db.TEXT))
    cont.append(db.Property("revision", datatype=db.TEXT))
    # create RecordTypes
    cont.append(db.RecordType("Software").add_property("author").add_property("revision"))
    cont.append(db.RecordType("State").add_property("x", importance=db.OBLIGATORY)
                .add_property("y").add_property("z"))
    cont.append(db.RecordType("Parameters").add_parent("State", inheritance=db.ALL))
    cont.append(db.RecordType("Result").add_parent("State", inheritance=db.RECOMMENDED))
    cont.append(db.RecordType("SoftwareRun").add_property("Software").add_property("Parameters")
                .add_property("completed").add_property("Result"))
    cont.insert()  # actually insert the Entities


def simulations(n, t_max):
    """Run the simulations.

    Parameters
    ----------
    n : int
      The number of runs.

    t_max : float
      The maximum time of integration.
    """

    software = (db.Record("simulator").add_parent("Software")
                .add_property("author", value="IndiScale GmbH")
                .add_property("revision", value="1234CDEF89AB"))
    software.insert()
    for i in range(n):
        # Get the parameters and result
        initial, result = run_simulation(run=i, t_max=t_max)

        # Prepare CaosDB insertion
        run = db.Record().add_parent("SoftwareRun").add_property("Software", value=software.id)
        parameters = (db.Record().add_parent("Parameters").add_property("x", initial[0])
                      .add_property("y", initial[1]).add_property("z", initial[2]))
        result_record = (db.Record().add_parent("Result").add_property("x", result[0])
                         .add_property("y", result[1]).add_property("z", result[2]))
        run.add_property("Parameters", value=parameters).add_property("Result", value=result_record)
        cont = db.Container()
        cont.extend([run, parameters, result_record])
        cont.insert()           # Insert everything of this run into CaosDB.


def run_simulation(run, t_max):
    """Integrate the Rössler attractor from random initial values."""
    a, b, c = (0.1, 0.1, 14)

    def diff(t, x):
        diff = np.array([-x[1] - x[2],
                         x[0] + a * x[1],
                         b + x[2] * (x[0] - c)])
        return diff

    x0 = np.random.uniform(-100, 100, 3)

    result = scipy.integrate.solve_ivp(diff, [0, t_max], x0)
    x = result.y[:, -1]
    return (x0, x)


def analyze():
    """Find the initial conditions which produce the smalles x,y values after the given time."""
    distance = 5
    data = db.execute_query("""SELECT Parameters, Result FROM RECORD SoftwareRun WITH
        (((Result.x < {dist}) AND (Result.x > -{dist}))
        AND (Result.y < {dist})) AND Result.y > -{dist}""".format(dist=distance))
    dataframe = to_table(data)  # Convert into a Pandas DataFrame

    parameters = db.Container().extend([db.Record(id=id) for id in dataframe.Parameters]).retrieve()

    initial_distances = [np.linalg.norm([p.get_property(dim).value for dim in ["x", "y", "z"]])
                         for p in parameters]

    print("These distances resulted in small x,y, values:\n{}".format(initial_distances))


def main():
    # 1. Set up the data model
    setup_caosdb()

    # 2. Run simulations
    simulations(n=200, t_max=5)

    # 3. Find initial conditions with interesting results
    analyze()


if __name__ == '__main__':
    main()
