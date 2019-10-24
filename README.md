# CLIJPY
CLIPY is a bridge between [CLIJ](https://clij.github.io) and 
[python](https://python.org) via 
[pyimagej](https://pypi.org/project/pyimagej/)

![Image](images/clijpy-screenshot.png)

Right now, this is very preliminary.

## Installation
Download and install [Fiji](https://fiji.sc) and activate the clij and clij2 (experimental) update sites as [described here](https://clij.github.io/clij-docs/installationInFiji). 
You will need to specify an ImageJ location later in your pyimagej scripts. Specify the installation directory of Fiji.
Futhermore, install [pyimage as described on its github page](https://github.com/imagej/pyimagej). 
In case that doesn't work, try the following procedures:

Download [python](https://python.org), 
install [pyjnius](https://pyjnius.readthedocs.io/en/stable/installation.html#) 
and [pyimagej](https://pypi.org/project/pyimagej/),
for example via [anaconda](https://www.anaconda.com/):



### Installation on Windows 10:
```bash
set PATH=%PATH%;C:\Program Files\Java\jdk1.8.0_161\jre\bin\server
copy "C:\Program Files\Java\jdk1.8.0_161\include\win32\jni_md.h" c:\ProgramData\Anaconda3\Library\include
python -m pip install --upgrade pip setuptools
python -m pip install --upgrade cython
pip install pyjnius
pip install pyimagej

set "JDK_HOME=C:\Program Files\Java\jdk1.8.0_161\"

pip install jnius

# get the environment.yml file from: https://raw.githubusercontent.com/imagej/pyimagej/master/environment.yml
conda env create -f environment.yml

conda activate imagej

pip install pyimagej
pip install scikit-image
pip install scipy
pip install numpy
pip install matplotlib
```

### Installation on Ubuntu Linux 18.04
[Download](https://docs.conda.io/en/latest/miniconda.html) and 
install [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).
Afterwards, restart your terminal and run these commands:
```
conda config --add channels conda-forge 
conda install pyimagej openjdk=8
conda create -n imagej pyimagej openjdk=8
conda activate imagej
conda install scikit-image
```

On some computers it might be necessary to install maven, python3, cython and a jdk. In this case these commands may help:
```bash
sudo apt-get install maven
sudo apt-get install python3-pip

sudo apt-get install cython
pip3 install Cython
sudo apt-get install default-jdk

```

## Example code
Examples are available in the [python](https://github.com/clij/clijpy/blob/master/python/) folder. 

After installation, you can call the examples like this:

```bash
conda activate imagej
python demo.py
```

Please note that you need to update the path to your Fiji installation in order to make the scripts run.

## Please note
It is recommended to [use clij from Fiji](https://clij.github.io/clij-docs/installationInFiji). 
Python support is under development.

[Back to CLIJ documentation](https://clij.github.io/)
