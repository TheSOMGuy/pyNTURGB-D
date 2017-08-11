#!/usr/bin/env python3

# Python module import
import sys
import os

# Ppe module import
import neuron as s_N
import kSOMtrain as training

import tkinter as tk
from tkinter import filedialog

class som():

	def __init__( self, verbose=False ):
		self.__neurons = []
		self.__initial_learnRate_ = 0.1
		self.__final_learnRate_ = 0.05
		self.__cycles_per_frame_ = 2
		self.__verbose = verbose

	def set_neurons( self, som ):
		self.__neurons = som

	def get_neurons( self ):
		return self.__neurons

	def load_from_file( self, _path_='som/basic_som/java_map_slim_with_legs_outstretched_arms.dat' ):
		
		# Open the som file.
		file_handler = open(_path_, 'r')

		# Read the content line by line and store it
		for line in file_handler:
			# Split the line
			splits = line.split(',')
			# Instantiate a new neuron
			neuron = s_N.som_neuron()
			# Fill the neuron ( neuronX, neuronY, neuronZ, anchorNeuron, neuronName, neighbours, features )
			neuron.set_neuron( splits[0], splits[1], splits[2], splits[3], "", [ splits[4], splits[5], splits[6], splits[7].split(';')[0] ], [] )
			# Store the neuron in the som 
			self.__neurons.append(neuron)

	def save_som_to_file( self ):

		# Generate the tk context for the store dialog
		root = tk.Tk()
		root.withdraw()

		# Get the path of your ppe script and add the trained som archive 
		store_path = os.getcwd() + "/som/trained_soms/"

		# Open a save dialog 
		f = filedialog.asksaveasfilename(initialdir=store_path, title="Store file", filetypes=((".dat files","*.dat"),("all files","*.*")))

		# asksaveasfile return `None` if dialog closed with "cancel".
		if f is None: 
			pass
		else:
			# Open the file
			file = open(f, 'w')

			# Step trough the list of neurons and add each part to a string which is then finally stored
			for neuron in self.__neurons:
				line = ""
				line = neuron.get_spatial_position()[0] + "," + neuron.get_spatial_position()[1] + "," + neuron.get_spatial_position()[2] + "," + neuron.get_anchor() + "," + neuron.get_name() 

				number_of_neighbours = len(neuron.get_neighbours())

				# Step trough the list of neighbours
				for i in range(0, number_of_neighbours ):
					line += neuron.get_neighbours()[i]
					if( i < number_of_neighbours - 1 ):
						line += ','
					else:
						# If it is the last neighbour add a ";" than a ","
						line += ';'

				if( self.__verbose == True ):
					print(line)

				file.write( line )
				line = ""
		
		file.close()

	def train_som( self, _data_, _initial_learn_rate_=0.1, _final_learn_rate_=0.05, _cycles_per_frame_=2 ):
		training.train( _data_, self.get_neurons() )


