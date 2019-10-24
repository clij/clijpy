# demo.py
#
# This example script show how to process image in the GPU via
# python, numpy, pyimagej and clij.
#
# Author: Robert Haase, rhaase@mpi-cbg.de
#         August 2019
#######################################################3333

# init pyimage to get access to jar files
import imagej
ij = imagej.init('C:/programs/fiji-win64/Fiji.app/')

# load some image data
from skimage import io
sk_img = io.imread('https://samples.fiji.sc/blobs.png')

# init clijpy to get access to the GPU
from jnius import autoclass
CLIJx = autoclass('net.haesleinhuepf.clijx.CLIJx')
clijx = CLIJx.getInstance();

# convert and array to an ImageJ2 img:
import numpy as np
np_arr = np.array(sk_img)
ij_img = ij.py.to_java(np_arr)

# push the image to the GPU
input = clijx.push(ij_img)
# allocate memory for the result image
output = clijx.create(input)

# blur the image
clijx.op.blur(input, output, 5.0, 5.0, 0.0);

# pull image back from GPU
ij_img_result = clijx.pull(output);
# convert to numpy/python
np_arr_result = ij.py.rai_to_numpy(ij_img_result);

# show the input and the result image
from matplotlib import pyplot as plt
plt.subplot(121)
plt.imshow(np_arr)
plt.subplot(122)
plt.imshow(np_arr_result)
plt.show()

print("Bye")