# GCODE-Arc-Converter

This is a simple python script that converts a series of G1 / G0 moves that form an arc into G2 / G3 arc moves.

## To Run This Script
* Clone the Repo.

* Create a virtual enviroment to run the bot. You can place it in the venv folder: 
```
python3 -m venv /venv/GCODE-venv
```

* Enter your virtual enviroment:
```
source /venv/GCODE-venv/bin/activate
```

* Install requirements:
```
pip3 install -r requirements.txt
``` 

* Adjust the `OUTPUT_FILE` in `the main.py` script.

* Run the script:
```
python3 main.py
```
