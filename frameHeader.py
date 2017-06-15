#!/usr/bin/env python3

import numpy as np

# Data structure for all joints of a frame.
class frameHeader(): 

	def __init__(self):
		self.__numberOfSkeletons = 0
		self.__skeleton_tracking_ID = 0
		self.__clipedEdges = 0
		self.__handLeftConfidence = 0
		self.__handLeftState = 0
		self.__handRightConfidence = 0
		self.__handRightState = 0
		self.__isRestricted = 0
		self.__leanX = 0.0
		self.__leanY = 0.0
		self.__bodyTrackingState = 0
		self.__numberOfJoints = 0
		self.__listOfJoints = []

	def set_Header( self,
		skeleton_tracking_ID, 
		clipedEdges, 
		handLeftConfidence, 
		handLeftState, 
		handRightConfidence, 
		handRightState, 
		isRestricted, 
		leanX, 
		leanY, 
		bodyTrackingState ):
			self.__skeleton_tracking_ID = skeleton_tracking_ID
			self.__clipedEdges = clipedEdges
			self.__handLeftConfidence = handLeftConfidence
			self.__handLeftState = handLeftState
			self.__handRightConfidence = handRightConfidence
			self.__handRightState = handRightState
			self.__isRestricted = isRestricted
			self.__leanX = leanX
			self.__leanY = leanY
			self.__bodyTrackingState = bodyTrackingState

	def set_NumberOfSkeletons( self, numberOfSkeletons ):
		self.__numberOfSkeletons = numberOfSkeletons

	def get_NumberOfSkeletons( self ):
		return self.__numberOfSkeletons 

	def set_NumberOfJoints( self, numberOfJoints ):
		self.__numberOfJonits = numberOfJoints

	def get_NumberOfJoints( self ):
		return self.__numberOfJonits

	def get_LeftHand( self ):
		return self.__handLeftConfidence, self.__handLeftState

	def get_RightHand( self ):
		return self.__handRightConfidence, self.__handRightState

	def get_Lean( self ):
		return self.__leanX, self.__leanY

	def get_SkeletonInformation(self):
		return self.__numberOfSkeletons, self.__skeleton_tracking_ID, self.__clipedEdges, self.__isRestricted, self.__bodyTrackingState, self.__numberOfJoints

	def set_ListOfJoints( self, listOfJoints ):
		self.__listOfJoints = listOfJoints

	def get_ListOfJoints( self ):
		return self.__listOfJoints

	# Compute the absolute amount of movement between two frames over all joints
	def ftf_joint_diff( self, _another_frame_ ):

		# Get the joints from the frames
		_own_joints_ = self.get_ListOfJoints()
		_another_joints_ = _another_frame_.get_ListOfJoints();

		# Create buckets for the world joint position
		_own_world_ = (0,0,0)
		_another_world_ = (0,0,0)

		# This is the bucket fpor the absoluit distance over all joints
		_ive_come_a_long_way_baby_ = 0.0

		for k in range(0, self.get_NumberOfJoints() ):

			# Get the world coordinates of each joint 
			_own_world_ = np.array(_own_joints_[k].get_WorldJoint())
			_another_world_ = np.array(_another_joints_[k].get_WorldJoint())
			
			# Compute the euclidean using numpy
			_ive_come_a_long_way_baby_ += np.linalg.norm( _own_world_ - _another_world_ )

		# Return the shizzle
		return _ive_come_a_long_way_baby_

