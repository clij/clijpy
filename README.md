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
conda config --add channels conda-forge
conda config --set channel_priority strict

conda create -n pyimagej pyimagej openjdk=8
Whenever you want to use pyimagej, activate its environment:

conda activate pyimagej
pip install pyimagej
pip install scikit-image
pip install scipy
pip install numpy
pip install matplotlib
pip install gputools
```

If installation of gputools doesn't work because of issues with pyopencl for Windows, consider downloading a precompiled wheel (e.g. from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/) ) and installing it manually. 

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
