# Data Models



You also want to change the datamodel? Also call
```bash
pip3 install --user --no-deps .
```
in 
```bash
CaosDB/data_models
```

Change to the appropriate directory
```bash
cd CaosDB/data_models
```
There are "data models" defined in 
```bash
caosdb_models
```
having an ending like "_model.py"
A set of data models is also considered to be a model
You can create an UML representation of a model or a set of models by calling
```bash
./model_interface.py -u model_name [model_name2]
```
If you have troubles look at
```bash
./model_interface.py -h
```
You can change existing models (but be careful! I hope you know what you are doing) or add new ones by changing the appropriate files or adding a new XXXX_model.py
Once you are done, you can sync your changes with the server
```bash
./model_interface.py -s model_name [model_name2]
```
