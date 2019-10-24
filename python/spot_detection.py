# spot_detection.py
#
# This example script show how to do spot detection and
# visualize in a 3D image on the GPU via python, numpy,
# pyimagej, clij and napari.
#
#
# Author: Robert Haase, rhaase@mpi-cbg.de
#         October 2019
######################################################

# init pyimage to get access to jar files
# The below mentioned Fiji installation sould have the
# update sites "clij" and "clij2" activated.
import imagej
ij = imagej.init('C:/programs/fiji-win64/Fiji.app/')

# load some image data
from skimage import io
sk_img = io.imread('../resources/Nantes_000646.tif')

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

# workflow configuration
factor = 1.0
backgroundSubtractionXY = 5
backgroundSubtractionZ = 0
blurXY = 3
blurZ = 3
maximumSearch = 1
thresholdAlgorithm = 'Otsu'
samplingFactor = [
    0.52 * factor,
    0.52 * factor,
    3 * factor
];

originalSize = clijx.getSize(input)
processingSize = [
    originalSize[0] * samplingFactor[0],
    originalSize[1] * samplingFactor[1],
    originalSize[2] * samplingFactor[2]
]

# allocate memory in GPU for proessing
downsampled = clijx.create(processingSize)
backgroundSubtracted = clijx.create(processingSize)
blurred = clijx.create(processingSize)
thresholded = clijx.create(processingSize)
detected = clijx.create(processingSize)
masked = clijx.create(processingSize)
labelled = clijx.create(processingSize)

# pre-process
clijx.downsample(input, downsampled, samplingFactor[0], samplingFactor[1], samplingFactor[2])
clijx.subtractBackground(downsampled, backgroundSubtracted, backgroundSubtractionXY, backgroundSubtractionXY, backgroundSubtractionZ)
clijx.blur(backgroundSubtracted, blurred, blurXY, blurXY, blurZ)

# 3D spot detection
clijx.detectMaximaBox(blurred, detected, maximumSearch)

# remove spots in background
clijx.automaticThreshold(blurred, thresholded, thresholdAlgorithm)
clijx.mask(detected, thresholded, masked)

# read out spot positions from spot stack
clijx.connectedComponentsLabeling(masked, labelled)
numberOfDetectedSpots = clijx.maximumOfAllPixels(labelled)
pointlist = clijx.create([numberOfDetectedSpots, labelled.getDimension()], input.getNativeType())
clijx.spotsToPointList(labelled, pointlist)

# get point coordinates from GPU and bring it in the right shape for napari
points = ij.py.rai_to_numpy(clijx.pull(pointlist))
points[[0, 1, 2], :] = points[[2, 1, 0],:]
points = np.transpose(points)

# pull image stacks back from GPU and convert them to numpy
np_masked_result = ij.py.rai_to_numpy(clijx.pull(masked))
np_thresholded_result = ij.py.rai_to_numpy(clijx.pull(thresholded))
np_image_result = ij.py.rai_to_numpy(clijx.pull(downsampled))

# view data and results with napari
import napari
with napari.gui_qt():
    # create a Viewer and add an image
    viewer = napari.view_image(np_image_result, rgb=False, colormap='green')
    viewer.add_image(np_masked_result, contrast_limits=[0, 1], name='mask', visible=False)
    viewer.add_image(np_thresholded_result, contrast_limits=[0, 1], name='spots', visible=False)

    size1 = np.array([7, 7, 7])
    viewed_points = viewer.add_points(points, size=size1)
    viewed_points.symbol = "+"
    viewed_points.edge_color = 'black'
    viewed_points.face_color = 'red'
    viewed_points.opacity = 0.5
    viewed_points.n_dimensional = True

print("Bye")