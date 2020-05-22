# PsychoPy Add-On
This tool is used to create onset files quickly and easily even being able to create an entire experiments onset files with a single click of a button. It is also used to output the time series using these onset files.

## Installation
Installing this application has two parts. Installing Kivy, and then all of the other dependecies.

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
pip install -r requirements.txt
```

## Contribution
This project was done for RUBIC by Michael Kochera.
