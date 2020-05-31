# PsychoPy Add-On
This tool is most useful if the data is organized in BIDS Format. It quickly and easily produces onset files even being able to create an entire experiments onset files with a single click of a button. It can also perform a batch BET Extraction and batch FEAT analysis on all subjects in an experiment but only if they are organized in the BIDS Format. The FEAT analysis utilizes fsl and requires an fsf file with the same number on EV's to run properly. Then all of the data is organized nicely into the Data directory that gets outputted by the end of running the tool.

## Installation
Installing this application has three parts. Installing Python3, Kivy, and then all of the other dependecies. Kivy requires the use the of python3 which most likely won't be the main python on your system being that fsl requires python2.

### Python3 Installation
All installations must be done in relation to python3 using pip3. Installation of python3 and pip3 can be done with the following:

```bash
sudo apt install python3
sudo apt-get install python3-pip
```

### Kivy Installation
Kivy installation differs depending on the OS. The basic installation of Kivy for the purposes of this app can be done with the following:

#### Linux
```bash
python -m pip install --upgrade --user pip setuptools
python -m pip install kivy
```

#### Windows
```bash
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
python -m pip install kivy_deps.gstreamer==0.1.*
python -m pip install kivy_deps.angle==0.1.*
python -m pip install kivy==1.11.1
```
#### Mac
```bash
python -m pip install kivy
```

For more information about Kivy and having more control in its installation, go to https://kivy.org/#download

### Requirments Installation
To install all of the dependencies but Kivy simply navigate to the directory with requirements.txt and run the following:
```bash
pip3 install -r requirements.txt
```

## Usage
The tool is meant to be used going down the displayed buttons one at a time. If the order is followed properly a Data directory will show up containing onset files, BET's, and a FEAT analysis for each subject.

## Run.py
To run the tool, navigate to the PsychAdd directory and run the following:
```bash
python3 run.py
```

## Contribution
This project was done for RUBIC by Michael Kochera.
