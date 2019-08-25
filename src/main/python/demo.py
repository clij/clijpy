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

# init clijpy to get access to the GUP
from jnius import autoclass
CLIJPY = autoclass('net.haesleinhuepf.clijpy.CLIJPY')
clijpy = CLIJPY.getInstance();

# convert and array to an ImageJ2 img:
import numpy as np
np_arr = np.array(sk_img)
ij_img = ij.py.to_java(np_arr)

# push the image to the GPU
input = clijpy.push(ij_img)
# allocate memory for the result image
output = clijpy.create(input)

# blur the image
Float = autoclass('java.lang.Float')
clijpy.op.blur(input, output, Float(5.0), Float(5.0), Float(0.0));

# pull image back from GPU
ij_img_result = clijpy.pull(output);
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