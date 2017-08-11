#!/usr/bin/env python3

# Python module import
import sys
import os
import numpy as np
import random as r_F

from numpy import array
from numpy import random
from PIL import Image

# Ppe module import
#import som_neuron as s_N

def train( _image_data_, _neurons_ ):

	spatials = []

	for neuron in _neurons_:
		spatials.append(neuron.get_spatial_position())

	# Open the specific image
	_org_image_ = Image.open(_image_data_[0], 'r')
	# Read the data
	np_data = array(_org_image_)
	# Get image dimension
	height, width  = np_data.shape

	# Create permutated index array for all rows
	randIDxY = np.arange(0, height)
	random.shuffle(randIDxY)

	# Create a column index array between 0 and width
	randIDxX = np.arange(0, width)

	# Step through the rows of the image
	for yIndex in randIDxY:
		# Permutated the column index array for each column
		random.shuffle(randIDxX)

		# Step trough the columns of the image
		for xIndex in randIDxX:
			pass		



