NOTE: Development of CLIJPY is on halt. Check out [py-clEsperanto](https://github.com/clEsperanto/pyclesperanto_prototype) for OpenCL-based GPU-accelerated image processing from python.

# CLIJPY
CLIPY is a bridge between [CLIJ](https://clij.github.io) and 
[python](https://python.org) via 
[pyimagej](https://pypi.org/project/pyimagej/)

![Image](images/clijpy-screenshot.png)

Right now, this is very preliminary.

## Installation
* Download and install [Fiji](https://fiji.sc)
* In Fiji, activate the clij and clij2 (experimental) update sites as [described here](https://clij.github.io/clij-docs/installationInFiji). 
* Restart Fiji.
You will need to specify an ImageJ location later in your pyimagej scripts. Specify the installation directory of Fiji.

* Futhermore, install [pyimagej as described on its github page](https://github.com/imagej/pyimagej):
```bash
conda config --add channels conda-forge
conda config --set channel_priority strict

conda create -n pyimagej pyimagej openjdk=8

conda activate pyimagej
pip install scikit-image scipy numpy matplotlib gputools
```

If installation of gputools doesn't work because of issues with pyopencl for Windows, consider downloading a precompiled wheel (e.g. from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl) ) and installing it manually:

```
pip install pyopencl-2019.1.1+cl12-cp37-cp37m-win_amd64.whl
pip install gputools
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

[Imprint](https://clij.github.io/imprint)
