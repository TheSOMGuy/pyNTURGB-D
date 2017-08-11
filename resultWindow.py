#!/usr/bin/env python3

# Pose estimation window class 

# Python module import

import sys
import time
import platform as pf
import tkinter as tk 
import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk 
from tkinter import Canvas
from numpy import array
from numpy import dstack
from bresenham import bresenham
import numpy.matlib as n_ml


# Ppe module import

import joint as j
import frameHeader as f_H

def draw_point( _data_, _depthY_, _depthX_ ):

	# first row
	_data_[_depthY_-1,_depthX_-1][0] = 255
	_data_[_depthY_-1,_depthX_-1][1] = 42
	_data_[_depthY_-1,_depthX_-1][2] = 0

	_data_[_depthY_-1,_depthX_][0] = 255
	_data_[_depthY_-1,_depthX_][1] = 42
	_data_[_depthY_-1,_depthX_][2] = 0

	_data_[_depthY_-1,_depthX_+1][0] = 255
	_data_[_depthY_-1,_depthX_+1][1] = 42
	_data_[_depthY_-1,_depthX_+1][2] = 0

	# second row
	_data_[_depthY_,_depthX_-1][0] = 255
	_data_[_depthY_,_depthX_-1][1] = 42
	_data_[_depthY_,_depthX_-1][2] = 0

	_data_[_depthY_,_depthX_][0] = 255
	_data_[_depthY_,_depthX_][1] = 42
	_data_[_depthY_,_depthX_][2] = 0

	_data_[_depthY_-1,_depthX_+1][0] = 255
	_data_[_depthY_-1,_depthX_+1][1] = 42
	_data_[_depthY_-1,_depthX_+1][2] = 0

	# third row

	_data_[_depthY_+1,_depthX_-1][0] = 255
	_data_[_depthY_+1,_depthX_-1][1] = 42
	_data_[_depthY_+1,_depthX_-1][2] = 0

	_data_[_depthY_+1,_depthX_][0] = 255
	_data_[_depthY_+1,_depthX_][1] = 42
	_data_[_depthY_+1,_depthX_][2] = 0

	_data_[_depthY_+1,_depthX_+1][0] = 255
	_data_[_depthY_+1,_depthX_+1][1] = 42
	_data_[_depthY_+1,_depthX_+1][2] = 0

	return _data_

# This function draws a line directly on the image grid.
# We use the bresenham algorithm for this ( https://pypi.python.org/pypi/bresenham )
def draw_connections( _data_, _list_of_Joints_ ):

	# from the original matlab scripts
	# in the skeleton structure, each joint is connected to some other joint:
	# connecting_joint = [2, 1, 21, 3, 21, 5, 6, 7, 21, 9, 10, 11, 1, 13, 14, 15, 1, 17, 18, 19, 2, 8, 8, 12, 12];

	# We use a modified connection list based on figure 1 in the paper. 
	#( The index starts at zero, also in the paper. This is confusing because the image claim something different. )
	# 
	# http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shahroudy_NTU_RGBD_A_CVPR_2016_paper.pdf
	# Adapted joint connections
	connections = [
		[0,1], 
		[1,20],
		[20,2],
		[2,3],
		[20,4],
		[4,5],
		[5,6],
		[6,7],
		[20,8],
		[8,9],
		[9,10],
		[10,11],
		[0,16],
		[16,17],
		[17,18],
		[18,19],
		[0,12],
		[12,13],
		[13,14],
		[14,15]] 

	# Get the depth coordinates for each pair in connections 
	# A pair is hold the indexes for the start and the end joint in the joint list
	for pair in connections:
		# Get the position of start end end joint.
		startX, startY = _list_of_Joints_[pair[0]].get_Depth()
		endX, endY = _list_of_Joints_[pair[1]].get_Depth()

		# Use the bresenham algorithm for computing the line on a rectangular grid between start and end point.
		# The function return the grid cells which will be drawn for the line.
		line = list( bresenham( int(startX), int(startY), int(endX), int(endY) ) )
		
		# Draw the line by coloring each grid cell from the bresenham algo.
		for pair in line:
			_data_[ pair[1], pair[0] ][0] = 0
			_data_[ pair[1], pair[0] ][1] = 0
			_data_[ pair[1], pair[0] ][2] = 255

	return _data_


def show_stream( _files_, _skeleton_frames_, verbose ):

	# The increment for the frame list
	_frame_increment_ = 0

	# Generate the root window
	root = tk.Tk()
	# Give em some geometry
	root.geometry('+%d+%d' % (100,100))

	# Iterate over images in list
	for _file_path_ in _files_:

		# If verbose is true: talk like my girlfriend after a long day of work and social interaction
		if( verbose == True ):
			print ( 'Processing: ', _file_path_ )

		# For window decoration purposes
		if sys.platform.startswith('linux'):
			_file_name_ = _file_path_.split('/')[1]
		elif sys.platform.startswith('win32'):
			_file_name_ = _file_path_.split('\\')[1]

		# Get the associated skeleton frame from the list
		_skeleton_frame_ = _skeleton_frames_[ _frame_increment_ ]

		# Increment the index operator for the next round
		_frame_increment_ += 1

		try:

			# Open the original file
			_org_image_ = Image.open(_file_path_, 'r')
			# Open depth file
			np_data = array(_org_image_)
			# https://github.com/shahroudy/NTURGB-D/blob/master/Matlab/show_skeleton_on_depthmaps.m 
			# depth maps are in millimeters we need to scale them to [0,255]
        	# for visualization:
			np_data = np.divide(np_data,5000)
			# Check if each value in the image matrix is smaller then 1 else set to 1
			np_data[np_data > 1] = 1
			# Convert the data to true grayvalues [0|255]
			np_data = np.dot(np_data, 255)
			np_data = np_data.astype('uint8')

			# Build the 3d RGB matrix ( also gray ) from the 1d gray matrix
			np_data = np.dstack((np_data, np_data, np_data))
	
			# Grab the list of associated joints for this frame			
			_list_of_Joints_ = _skeleton_frame_.get_ListOfJoints()

			# Step trough the list
			for j in _list_of_Joints_:
				# Grab the position of each joint in the masked depth image
				_depthX_, _depthY_ = j.get_Depth()
				# Cast to int because X and Y are floats ( from the original files )
				_depthX_ = int(_depthX_)
				_depthY_ = int(_depthY_)

				# Draw directly in the 3 channel RGB image we created earlier
				draw_point( np_data, ( _depthY_ ), ( _depthX_ ) )
				
			draw_connections( np_data, _list_of_Joints_ )

			# Create an imageTK photo image object ( 3x8 bit, true color) for visualisation
			_final_depth_image_ = Image.fromarray(np_data, 'RGB')
			tkpi = ImageTk.PhotoImage( _final_depth_image_ )

			# label the root window with the image name
			label_image = tk.Label(root, image=tkpi)
			label_image.place(x=0,y=0,width=_org_image_.size[0],height=_org_image_.size[1])
			root.title( _file_name_ )
		
			# Adapt the window geometry to the image specs
			root.geometry('%dx%d' % (_org_image_.size[0],_org_image_.size[1]))

			root.update()
			# Take your timne to enjoy the image
			time.sleep(.040)
		except Exception as e:
			# This is used to skip anything not an image.
			# Image.open will generate an exception if it cannot open a file.
			# Warning, this will hide other errors as well.
			if( verbose == True ):
				print ('There was an exception in: ', _file_path_ )
				# Print the exception message ( yep, it's useful )
				print ('Exceptinon: ',e)
			pass
