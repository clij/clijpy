# nantes.py
#
# This example script show how to process image in the GPU via
# python, numpy, pyimagej and clij.
#
# Author: Robert Haase, rhaase@mpi-cbg.de
#         October 2019
#######################################################3333

# init pyimage to get access to jar files
import imagej
ij = imagej.init('C:/programs/fiji-win64/Fiji.app/')

# load some image data
from skimage import io
sk_img = io.imread('C:/structure/code/clatlab/src/test/resources/Nantes_000646.tif')

# init clijpy to get access to the GUP
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
Float = autoclass('java.lang.Float')
# clijx.op().blur(input, output, Float(5.0), Float(5.0), Float(0.0));

# workflow configuration
factor = 1.0;
backgroundSubtractionXY = Float(5);
backgroundSubtractionZ = Float(0);
blurXY = Float(3);
blurZ = Float(3);

Integer = autoclass('java.lang.Integer')
maximumSearch = Integer(1);
thresholdAlgorithm = 'Otsu';

samplingFactor = [
    0.52 * factor,
    0.52 * factor,
    3 * factor
];
originalSize = clijx.op.getSize(input)
processingSize = [
    originalSize[0] * samplingFactor[0],
    originalSize[1] * samplingFactor[1],
    originalSize[2] * samplingFactor[2]
]

downsampled = clijx.create(processingSize);
backgroundSubtracted = clijx.create(processingSize);
blurred = clijx.create(processingSize);
thresholded = clijx.create(processingSize);
detected = clijx.create(processingSize);
masked = clijx.create(processingSize);
labelled = clijx.create(processingSize);
# preprocess
clijx.op.downsample(input, downsampled, Float(samplingFactor[0]), Float(samplingFactor[1]), Float(samplingFactor[2]));
clijx.op.subtractBackground(downsampled, backgroundSubtracted, backgroundSubtractionXY, backgroundSubtractionXY, backgroundSubtractionZ);
clijx.op.blur(backgroundSubtracted, blurred, blurXY, blurXY, blurZ);

# 3D spot detection
clijx.op.detectMaximaBox(blurred, detected, maximumSearch);

# remove spots in background
clijx.op.automaticThreshold(blurred, thresholded, thresholdAlgorithm);
clijx.op.mask(detected, thresholded, masked);
clijx.op.connectedComponentsLabeling(masked, labelled);

# read out spot positions
numberOfDetectedSpots = clijx.op.maximumOfAllPixels(labelled);
pointlistSize = [numberOfDetectedSpots, labelled.getDimension()];
print(pointlistSize)
pointlist = clijx.create(pointlistSize, input.getNativeType());
clijx.op.spotsToPointList(labelled, pointlist);

pointsRAI = clijx.pull(pointlist)
points = ij.py.rai_to_numpy(pointsRAI);
points[[0, 1, 2], :] = points[[2, 1, 0],:]
points = np.transpose(points)
print(points)

# pull image back from GPU and convert it to numpy
masked_result = clijx.pull(masked);
np_masked_result = ij.py.rai_to_numpy(masked_result);

thresholded_result = clijx.pull(thresholded);
np_thresholded_result = ij.py.rai_to_numpy(thresholded_result);

image_result = clijx.pull(downsampled);
np_image_result = ij.py.rai_to_numpy(image_result);

# show the input and the result image
# from matplotlib import pyplot as plt
# plt.subplot(121)
# plt.imshow(np_arr)
# plt.subplot(122)
# plt.imshow(np_arr_result)
# plt.show()

import napari

# create Qt GUI context
with napari.gui_qt():
    # create a Viewer and add an image
    viewer = napari.view_image(np_image_result, rgb=False)
    viewer.add_image(np_masked_result, contrast_limits=[0, 1], name='mask')
    viewer.add_image(np_thresholded_result, contrast_limits=[0, 1], name='spots')
    size1 = np.array([3, 3, 3])
    viewer.add_points(points, size=size1)

    #viewer.add_points(
    #    points, face_color='blue', n_dimensional=True
    #)

print("Bye")