# To import Python modules
import Pkg; Pkg.add("PyCall")

# import pyCaosDB
using PyCall; @pyimport caosdb

ExpType = caosdb.RecordType(name="MyExperimentType")
