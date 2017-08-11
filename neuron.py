#!/usr/bin/env python3

# Python module import
import sys
import os

# Ppe module import

class som_neuron():

	def __init__(self):
		self.__neuronX = 0.0
		self.__neuronY = 0.0
		self.__neuronZ = 0.0
		self.__name = ""
		self.__neighbours = []
		self.__features = []

	def set_neuron(self,
		neuronX,
		neuronY,
		neuronZ,
		anchor,
		name = [],
		neighbours = [],
		features = []
		):
			self.__neuronX = neuronX
			self.__neuronY = neuronY
			self.__neuronZ = neuronZ
			self.__anchor = anchor
			self.__name = name
			self.__neighbours = neighbours
			self.__features = features

	def set_spatial_position( self, neuronX, neuronY, neuronZ ):
		self.__neuronX = neuronX
		self.__neuronY = neuronY
		self.__neuronZ = neuronZ

	def get_spatial_position( self ):
		return self.__neuronX, self.__neuronY, self.__neuronZ

	def set_anchor( self, anchor ):
		self.__anchor = anchor

	def get_anchor( self ):
		return self.__anchor

	def set_name( self, name ):
		self.__name = name

	def get_name( self ):
		return self.__name 

	def set_neighbours( self, neighbours ):
		self.__neighbours = neighbours

	def get_neighbours( self ):
		return self.__neighbours

	def set_features( self, features ):
		self.__features = features      

	def get_features( self ):
		return self.__features
