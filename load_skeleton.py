#!/usr/bin/env python3

# Python module import
import numpy as np

# Ppe module import
import joint as j
import frameHeader as fHeader

# Reads the data for a complete frame set from the NTU RGB+D Action Recognition Dataset
# Included joints are: 
# --------------------------------------------------------------------------------------------------------------
# 	0 -  base of the spine 
# 	1 -  middle of the spine
# 	2 -  neck 
#	3 -  head 
# 	4 -  left shoulder 
# 	5 -  left elbow 
# 	6 -  left wrist 
# 	7 -  left hand 
# 	8 -  right shoulder 
# 	9 - right elbow 
# 	10 - right wrist 
# 	11 - right hand 
# 	12 - left hip 
# 	13 - left knee 
# 	14 - left ankle 
# 	15 - left foot 
# 	16 - right hip 
# 	17 - right knee 
# 	18 - right ankle 
# 	19 - right foot 
# 	20 - spine 
#	21 - tip of the left hand 
# 	22 - left thumb 
# 	23 - tip of the right hand 
# 	24 - right thumb
# --------------------------------------------------------------------------------------------------------------

def read_skeleton_data( _file_Handler_, _verbose_ ):

	# Finally store all Frames ( with included joints per frame ) in this lists 
	frames_of_the_set = []
	frames_2_of_the_set = []

	# Number of Skeletons in the set
	nOSkel = 0

	raw_Content = []

	# Read the whole file in a data block.
	raw_Content = _file_Handler_.readlines()
	
	# Get the number of Frames
	number_of_frames = 0
	number_of_frames = raw_Content[0]
	if( _verbose_ == True):
		print( "Number of frames in the set: ", number_of_frames )      

	# Cut the first line ( number of frames ) from the raw_Content
	raw_Content = raw_Content[1:]
	if( _verbose_ == True ):
		print('Number of Skeletons: ', raw_Content[0] ) 

	# Adapt the increment for the subsequent for loop to the number of skeletons in the set.
	if( int(raw_Content[0]) == 1  ):
		forIncrement = 28
		noSkel = 1
	else:
		forIncrement = 55 
		noSkel = 2

	# Temporary data storages for the skeletons
	skeleton1 = []
	skeleton2 = []
	skeletal_block = []

	# Step through the lines of raw_Content and parse them
	for lineIdx in range(0, len(raw_Content), forIncrement ):

		# Get the n-th frame of the whole set.
		skeletal_block = []
		# Load frame wise the skeleton data ( a block contains one or two skeleton(s) )
		skeletal_block = raw_Content[lineIdx:lineIdx+forIncrement]

		# Depending on the number of skeletons in the frame build one list for a single skeleton set or two lists for a multiskeleton set.
		if( noSkel == 1 ):
			skeleton1 = store_skeleton(skeletal_block)
			frames_of_the_set.append( skeleton1 )
		if( noSkel == 2):
			# Get the first skeleton.
			skeleton1 = skeletal_block[0:28]
			#print('\n\n skeleton1: ', skeleton1 ) 
			frames_of_the_set.append( store_skeleton(skeleton1 ) )
			# Get the second skeleton.
			skeleton2 = skeletal_block[28:]
			#print('\n\n skeleton2: ', skeleton2 ) 
			frames_2_of_the_set.append( store_skeleton(skeleton2 ) )

	# # If more than one skeleton is in the set check for the primary one 
	dist_skel_1 = 0.0
	dist_skel_2 = 0.0
	if( noSkel > 1 ): 
		dist_skel_1, dist_skel_2 = check_for_primary_skeleton( frames_of_the_set, frames_2_of_the_set, _verbose_ )

	export_frames = []
	if( noSkel == 1 ):
		export_frames = frames_of_the_set
	else:
		# Depending on the distance the joints have moved decide which skeleton is the primary one
		if dist_skel_1 > dist_skel_2:
			export_frames = frames_of_the_set
		else:
			export_frames = frames_2_of_the_set

	# Nothing to say here. If so -> go study your shit
	return export_frames

# Depending on the distance which all joints have moved together 
# ( over all frames sum up all joint distances between two frames per skeleton ) 
# decide which skeleton is the primary one.
def check_for_primary_skeleton( _frames_of_the_set_, _frames_2_of_the_set_, verbose ):
	
	dist1 = 0.0
	dist2 = 0.0

	# Modus: Frame k+1 - Frame k ( of the same skeleton indicated by the skeleton id )
	for k in range(0, len(_frames_of_the_set_) - 1 ):
			dist1 += _frames_of_the_set_[k+1].ftf_joint_diff( _frames_of_the_set_[k] )

	for k in range(0, len(_frames_2_of_the_set_) - 1 ):
			dist2 += _frames_2_of_the_set_[k+1].ftf_joint_diff( _frames_2_of_the_set_[k] )

	# Explain the decision
	if( verbose == True ):
		print( '#### Moved distance per skeleton ####')
		print( "Dist1: ",dist1)
		print( "Dist2: ",dist2)
		print('\n\n')

	return dist1, dist2

def store_skeleton( _data_ ):

	# Initialize the header at this point because the number of observed skeletons is the first entry
	single_frame_header = fHeader.frameHeader()

	# Generate a new list for the to this frame associated joints
	joints_per_frame = []

	for lineIdx in range( 0, len(_data_) ):

		# Take a line from the raw data.
		single_line = _data_[lineIdx]

		# Cut trailing line break
		single_line.rstrip('\n')
		# Split the line to tokens using the whitespaces as delimiter
		single_Tokens = single_line.split(' ')

		# Special header numbers
		if( len(single_Tokens) == 1 ):
			# Number of observed skeleton
			if ( int(single_Tokens[0]) < 25 ):
				single_frame_header.set_NumberOfSkeletons(int(single_Tokens[0]))
			# Number of tracked joints in the frame
			elif( int(single_Tokens[0]) >= 25 ):
				single_frame_header.set_NumberOfJoints(int(single_Tokens[0]))
		
		# Store the header for each frame             
		if( len(single_Tokens) == 10 ):
			single_frame_header.set_Header( 
				int(single_Tokens[0]), 
				int(single_Tokens[1]),
				int(single_Tokens[2]), 
				int(single_Tokens[3]),
				int(single_Tokens[4]),
				int(single_Tokens[5]), 
				int(single_Tokens[6]),
				float(single_Tokens[7]),
				float(single_Tokens[8]),
				int(single_Tokens[9])
			)

		# Store the data of each joint from a frame
		if( len(single_Tokens) == 12 ):
			single_joint = j.joint()
			single_joint.set_Joint( 
				float(single_Tokens[0]),
				float(single_Tokens[1]),
				float(single_Tokens[2]),
				float(single_Tokens[3]),
				float(single_Tokens[4]),
				float(single_Tokens[5]),
				float(single_Tokens[6]),
				float(single_Tokens[7]),
				float(single_Tokens[8]),
				float(single_Tokens[9])
,				float(single_Tokens[10]),
				float(single_Tokens[11])
			)
			# Store the single joint in a list of joints for the frame
			joints_per_frame.append(single_joint)

		single_frame_header.set_ListOfJoints( joints_per_frame )

	#print(single_frame_header.get_SkeletonInformation())		
	return single_frame_header