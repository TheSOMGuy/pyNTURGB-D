#!/usr/bin/env python3

# Data class for a single joint.
class joint(): 

	def __init__(self):			
		self.__jointX = 0.0
		self.__jointY = 0.0
		self.__jointZ = 0.0
		self.__depthX = 0.0
		self.__depthY = 0.0
		self.__colorX = 0.0
		self.__colorY = 0.0
		self.__orientationW = 0.0
		self.__orientationX = 0.0
		self.__orientationY = 0.0
		self.__orientationZ = 0.0
		self.__jointTrackingState = 0

	def set_Joint( self, 
		jointX, 
		jointY, 
		jointZ, 
		depthX, 
		depthY, 
		colorX,
		colorY,
		orientationW, 
		orientationX, 
		orientationY, 
		orientationZ, 
		jointTrackingState ):
			self.__jointX = jointX
			self.__jointY = jointY
			self.__jointZ = jointZ	
			self.__depthX = depthX
			self.__depthY = depthY
			self.__colorX = colorX
			self.__colorY = colorY
			self.__orientationW = orientationW
			self.__orientationX = orientationX
			self.__orientationY = orientationY
			self.__orientationZ = orientationZ	
			self.__jointTrackingState = jointTrackingState		

	def set_WorldJoint( self, jointX, jointY, jointZ ):
		self.__jointX = jointX
		self.__jointY = jointY
		self.__jointZ = jointZ

	def get_WorldJoint(self):
		return self.__jointX, self.__jointY, self.__jointZ

	def set_Depth( self, depthX, depthY ):
		self.__depthX = depthX
		self.__depthY = depthY

	def get_Depth(self):
		return self.__depthX, self.__depthY

	def set_Color( self, colorX, colorY ):
		self.__colorX = colorX
		self.__colorY = colorY

	def get_Depth(self):
		return self.__depthX, self.__depthY
		
	def set_Orientation( self, orientationW, orientationX, orientationY, orientationZ ):
		self.__orientationW = orientationW
		self.__orientationX = orientationX
		self.__orientationY = orientationY
		self.__orientationZ = orientationZ

	def get_Orientation( self ):
		return self.__orientationW, self.__orientationX, self.__orientationY, self.__orientationZ 

	def set_JointTrackingState( self, jointTrackingState ):
		self.__jointTrackingState = jointTrackingState

	def get_JointTrackingState( self ):
		return self.__jointTrackingState