# GCODE-Arc-Converter

This is a simple python script that converts a series of G1 moves that form an arc into G2 / G3 arc moves. This can be benificial for 3D printers with small buffers or for STLs where the triangulation of the file is visable as a print defect. This script will also siginificantly reduce gcode file sizes. 

## To Run This Script
## From Release
Download and run the latest released version from the releases page. 
## From Source
* Ensure python 3.7 or later is installed on your system.

* Clone or download the repo.

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

* Adjust the `INPUT_FILE` in `the main.py` script.

* Run the script:
```
python3 main.py
```
