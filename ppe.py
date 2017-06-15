#!/usr/bin/env python3

# Python module import

import sys
import os
import math as ma
import argparse

# Ppe module import

import load_skeleton as l_S
import load_masked_depth as l_MD
import resultWindow as r_W
import som as som
import hoj3d as h3d
import hoj3d_tester as h3d_t

def main():
	path_name = ""
	som_path = ""
	show_stream = False
	verbose = False

	# Parse the command line options.
	path_name, skeleton_name, som_path, show_stream, verbose = parseOpts( sys.argv )

	# Build the skeleton filename string
	_skeleton_filename_ = skeleton_name + '.skeleton'
	
	# Build the associated masked depth directory pathname
	_masked_depth_pathname_ = path_name

	# ----------------------------------------------------------------------------------------------------
	# Load the initial SOM 
	if( os.path.isfile( som_path ) == True ):

		# Instantiate a new som
		_som_ = som.som()

		# Load the som data from the specified file.
		_som_.load_from_file( som_path )

	else:
		print("\nNo som file with name: ", som_path )
		print("Leave script now.\n")
		exit(0)

	# ----------------------------------------------------------------------------------------------------
	# Open the skeleton file if it exist.
	if( os.path.isfile( _skeleton_filename_ ) == True ):
		print( "Skeleton file: ", _skeleton_filename_ )
		_skeleton_fileHandler_ = open( _skeleton_filename_ , 'r')

		# Read the data from the skeleton file for the whole sequence
		all_skeleton_frames = l_S.read_skeleton_data( _skeleton_fileHandler_, verbose )

	else:
		print("\nNo skeleton file with name: ", _skeleton_filename_ )
		print("Leave script now.\n")
		exit(0)

	# ----------------------------------------------------------------------------------------------------
	# Open associated masked depth files in a directory with the same name as the skeleton file
	if( os.path.isdir( _masked_depth_pathname_ ) == True ):
		print( "Open masked depth files in: ", _masked_depth_pathname_ )

		# Read the data from the masked depth directory
		all_masked_depth_frames = l_MD.read_masked_depth_data( _masked_depth_pathname_ )

	else:
		print("\nNo depth mask directory with name: ", _masked_depth_pathname_ )
		print("Leave script now.\n")
		exit(0)

	# ----------------------------------------------------------------------------------------------------
	# Train the SOM with the data
	if( _som_ ):
		_som_.train_som( all_masked_depth_frames )
	else:
		pass


	# ----------------------------------------------------------------------------------------------------
	# Moin Franz,
	# Ich hab dir hier den Funktionsaufruf für die Hoj3D Funktion schon definiert.
	# Du brauchst dafür nur die Skeleton daten als Input. ( Soweit ich mich erinnere )
	# Aufbau der Daten:
	#
	#	 all_skeleton_frames ( liste von frames )
	#					|_> jeder Frame enthält den Frame_header und eine Liste von Joints des zugehörigen Skeletons 
	#
	#	-> frameHeader.py und joint.py sollten dir weitere Informationen dazu liefern
	#	-> Sollten weitere Fragen auftauchen -> schreib mir ne Mail, ich versuch sie trotz Urlaub so schnell wie möglich zu 
	#	   beantworten
	#
	#	# Franz 

	i = 0
	for frame in all_skeleton_frames:
		list_of_joints = frame.get_ListOfJoints()

		# gget joints from the paper 3, 5, 9, 6, 10, 13, 17, 14, 18, 12, 16
		# joints_to_compute = []
		# joints_to_compute.append(list_of_joints[3])		# head 		0
		# joints_to_compute.append(list_of_joints[5])		# l elbow	1
		# joints_to_compute.append(list_of_joints[9])		# r elbow	2
		# joints_to_compute.append(list_of_joints[6])		# l hand 	3
		# joints_to_compute.append(list_of_joints[10])		# r hand 	4
		# joints_to_compute.append(list_of_joints[13])		# l knee 	5
		# joints_to_compute.append(list_of_joints[17])		# r knee 	6
		# joints_to_compute.append(list_of_joints[14])		# l feet 	7
		# joints_to_compute.append(list_of_joints[18])		# r feet 	8
		# joints_to_compute.append(list_of_joints[12])		# l hip 	9
		# joints_to_compute.append(list_of_joints[16])		# r hip 	10

 		# hip center, spine, hip right, hip left
		hoj3d_set = h3d.compute_hoj3d(
			list_of_joints, 
			list_of_joints[0], 
			list_of_joints[1], 
			list_of_joints[16], 
			list_of_joints[12], 
			joint_indexes=[3, 5, 9, 6, 10, 13, 17, 14, 18, 12, 16], 
			use_triangle_function=True)


		filename = "{0:0=3d}".format(i)
		h3d_t.write_hoj3d(filename,hoj3d_set)
		i += 1
		# break
	#
	# ----------------------------------------------------------------------------------------------------

	# Let the show begin
	if show_stream == True:
		r_W.show_stream( all_masked_depth_frames, all_skeleton_frames, verbose )

# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# Parse the command line arguments
def parseOpts( argv ):

	skeleton_name = ""

	# generate parser object
	parser = argparse.ArgumentParser()
	# add arguments to the parser so he can parse the shit out of the command line
	parser.add_argument("-pn", "--part_name", action='store', dest='dataset_name', help="The name of part of the dataset.")
	parser.add_argument("-sp", "--som_path", action='store', dest='som_path', help="The absoult path to the self-organizing map u want to use.")
	parser.add_argument("-ss", "--show_stream", action='store_true', dest='show_stream', help="True if you want to see the image stream.")
	parser.add_argument("-v", "--verbose", action='store_true', dest='verbose', default='False', help="True if you want to listen to the chit-chat.")

	# finally parse the command line 
	args = parser.parse_args()

	print("\n\nInformation: ---------------------------------------------------------------------------------------------------------------")

	# code block for what to do if an argument passed the parsing
	if args.dataset_name:
		path_name = "data/" + args.dataset_name
		skeleton_name = "skeleton/" + args.dataset_name
	else: 
		path_name = "data/S001C001P001R001A001"
		skeleton_name = "skeleton/S001C001P001R001A001"
		print ("\nNo set path defined. Falling back to default path  : ", path_name )

	if args.som_path:
		som_path = args.som_path
	else: 
		som_path = "som/basic_soms/java_map_slim_with_legs_outstretched_arms.dat"
		print ("\nNo SOM defined. Falling back to default SOM        : ", som_path )


	print ("\nConfiguration:")
	print ("----------------------------------------------------------------------------------------------------------------------------")
	print ("Set          : ", path_name)
	print ("SOM          : ", som_path)
	print ("ShowStream   : ", args.show_stream)
	print ("verbose      : ", args.verbose)

	return path_name, skeleton_name, som_path, args.show_stream, args.verbose

# ----------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	main()