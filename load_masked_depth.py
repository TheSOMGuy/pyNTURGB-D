#!/usr/bin/env python3

import os

# Reads the content of an directory as a list of filenames and returns the list
def read_masked_depth_data( path ):

	masked_depth_frames = []

	for dir_item in os.listdir(path):
		dir_item_path = os.path.join(path, dir_item)
		if os.path.isfile(dir_item_path):
			with open(dir_item_path, 'r') as f:
				masked_depth_frames.append(dir_item_path)

	masked_depth_frames.sort()
	return masked_depth_frames