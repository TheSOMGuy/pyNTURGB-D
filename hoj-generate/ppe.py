#!/usr/bin/env python3

# Python module import

import sys
import os
import math as ma
import argparse

# Ppe module import

import load_skeleton as l_S
import hoj3d2 as h3d
import hoj3d_tester as h3d_t


def main():
	path_name = ""
	som_path = ""
	show_stream = False
	store_net = False
	verbose = False

	# Parse the command line options.
	path_name, skeleton_name, som_path, show_stream, store_net, verbose = parseOpts( sys.argv )

	files = os.listdir("../skeleton")
	i = 0
	if skeleton_name is not None:
		i = files.index(skeleton_name)
	for file in files[i:]:
		if file[0] is '#':
			continue
		
		_skeleton_filename_ = "../skeleton/" + file

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

		if os.path.exists(os.path.splitext(file)[0]):
			os.makedirs(os.path.splitext(file)[0])

		time = 0.0
		# test
		#for a in range(100):
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
			
			print(list_of_joints)
			print('\n')

			hoj3d_set,time = h3d.compute_hoj3d(list_of_joints, list_of_joints[0], list_of_joints[1], list_of_joints[16], list_of_joints[12], joint_indexes=[3, 5, 9, 6, 10, 13, 17, 14, 18], use_triangle_function=True, n_time = time) # hip center, spine, hip right, hip left

			# testing
			test_filename = os.path.splitext(file)[0] + "/" + os.path.splitext(file)[0] + "_{0:0=3d}".format(i)
			h3d_t.write_hoj3d(test_filename,hoj3d_set)
			i += 1
			# break
		# print(time)


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
	parser.add_argument("-sn", "--save_net", action='store_true', dest='save_net', default='False', help="True if you want to store the trained neural net.")

	# finally parse the command line 
	args = parser.parse_args()

	print("\n\nInformation: ---------------------------------------------------------------------------------------------------------------")

	# code block for what to do if an argument passed the parsing
	if args.dataset_name:
		path_name = "data/" + args.dataset_name
		skeleton_name = args.dataset_name + ".skeleton"
	else: 
		path_name = "data/S001C001P001R001A001"
		skeleton_name = None
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
	print ("Store NN     : ", args.save_net)
	print ("verbose      : ", args.verbose)

	return path_name, skeleton_name, som_path, args.show_stream, args.save_net, args.verbose

# ----------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	main()