#!/usr/bin/env python3

# Python module import
import numpy as np
import math as ma
import time


# Ppe module import
import frameHeader
import joint


# Die Basisfunktion des Modules
def compute_hoj3d( list_of_joints, reference_join, reference_join_up, reference_join_left, reference_join_right, joint_indexes = [], use_triangle_function = False, n_time = 0.0):

	t0 = time.time()

	# bins for alpha, the horizontal angle, starting from 
	alpha_bin = [0,30,60,90,120,150,180,210,240,270,300,330,360]
	# bins tor theta, the vertical angle, starting from north pole
	theta_bin = [-15,15,45,75,105,135,165,195]

	# the historamm of joints 3D
	hoj3d = [[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0]]

	# get joints to compute
	if(joint_indexes):
		joints_to_compute = []
		for index in joint_indexes:
			joints_to_compute.append(list_of_joints[index])
	else:
		joints_to_compute = list_of_joints
	

	# assign probability function
	probability_function = p_function
	if(use_triangle_function):
		probability_function = trinangle_function

	#translation
	translation_vector = np.array([-reference_join.get_WorldJoint()[0], -reference_join.get_WorldJoint()[1], -reference_join.get_WorldJoint()[2]])

	# print(translation_vector)

	for joint in joints_to_compute:
		point = np.array(joint.get_WorldJoint())
		transformed_point = point + translation_vector
		joint.set_WorldJoint(transformed_point.item(0),transformed_point.item(1),transformed_point.item(2))
	
	#
	# X = right_hip to left_hip
	#
	# Y = bottom_center to spine
	# 		(allmost perpendicular to alpha)
	#
	x_vector = np.array(reference_join_left.get_WorldJoint()) - np.array(reference_join_right.get_WorldJoint())
	y_vector = np.array(reference_join_up.get_WorldJoint()) - np.array(reference_join.get_WorldJoint())

	# calculate z
	z_vector = np.cross(x_vector,y_vector)

	# recalculate y so it is perpendicular to XZ plane
	y_vector = np.cross(z_vector,x_vector)

	for joint in joints_to_compute:
		r,alpha,theta = transform_coordinate(x_vector,y_vector,z_vector,joint.get_WorldJoint())
		
		j = 0
		for t in theta_bin:
			if(t >= 180):
				break

			# find theta-bins to calculate
			if((theta - t > 60) or (theta - t < -30)):
				j+=1
				continue

			i = 0
			for a in alpha_bin:
				if(a == 360):
					break

				# find alpha-bins to calculate
				if((alpha - a <= 60) and (alpha - a >= -30)):
					probability = abs((probability_function(alpha,(alpha_bin[i+1]+alpha_bin[i])/2))) * abs((probability_function(theta,(theta_bin[j+1]+theta_bin[j])/2)))

					# print(probability)
					hoj3d[j][i] += probability

				# wrap around the sphere
				if((alpha+360 - a <= 60) or (alpha-360 - a >= -30)):
					if(alpha < 30):
						probability = abs((probability_function(alpha+360,(alpha_bin[i+1]+alpha_bin[i])/2))) * abs((probability_function(theta,(theta_bin[j+1]+theta_bin[j])/2)))

						# print(probability)
						hoj3d[j][i] += probability
					elif(alpha > 330):
						probability = abs((probability_function(alpha-360,(alpha_bin[i+1]+alpha_bin[i])/2))) * abs((probability_function(theta,(theta_bin[j+1]+theta_bin[j])/2)))
						
						# print(probability)
						hoj3d[j][i] += probability

				i += 1
			j += 1

	# debug print
	#np.set_printoptions(precision = 3,suppress = True)
	#print(np.array(hoj3d))

	#hoj = np.array(hoj3d)
	#print(hoj.sum())

	t1 = time.time()
	n_time += t1 - t0

	return hoj3d,n_time

def transform_coordinate(x,y,z,vector):
	vector = np.array(vector)
	x = np.array(x)
	y = np.array(y)
	z = np.array(z)

	# for alpha:
	# project vector on ground plane
	# 
	# vector_p = vector_v + u * vector_y    => normal on the plane
	#
	# 0 = [vector_p - vector_x] * vector_y  => plane in normal form
	#
	# => 0 = [vector_v + u * vector_y - vector_x] * vector_y
	# => 0 = vector_v * vector_y + u * vector_y * vector_y - vector_x * vector_y
	# => u = (vector_x * vector_y - vector_v * vector_y) / (vector_y * vector_y)

	u = (np.dot(x,y) - np.dot(vector,y)) / np.dot(y,y)

	projected_vector = vector + u * y

#	print(projected_vector)

	r = ma.sqrt((vector * vector).sum())
	projected_r = ma.sqrt((projected_vector * projected_vector).sum())
	x_len = ma.sqrt((x * x).sum())
	y_len = ma.sqrt((y * y).sum())
	z_len = ma.sqrt((z * z).sum())

	cos_alpha = np.dot(x,vector) / (projected_r * x_len)
	cos_beta  = np.dot(z,vector) / (projected_r * z_len)
	cos_theta = np.dot(y,vector) / (r * y_len)

	# print(cos_alpha)

	alpha = ma.acos(cos_alpha) * 360 / (2 * ma.pi)
	if(cos_beta < 0):			# if vector is to the right of x
		alpha = 360 - alpha

	theta = ma.acos(cos_theta) * 360 / (2 * ma.pi)

	if(ma.isnan(alpha)):
		alpha = 0
	if(ma.isnan(theta)):
		theta = 0

	return r, alpha, theta

def p_function(x,my):

	# original
	# p = (1 / (ma.sqrt(2 * ma.pi))) * ma.pow(ma.e,(-0.5 * (x-my) * (x-my)))
	# changed
	p = ma.exp(-0.005 * (x-my) * (x-my))

	#print(x)
	#print(my)
	#print(p)

	return p

def trinangle_function(x,my):

	if(x < my):
		p = (x - my + 30) / 30
	else:
		p = (-x + my + 30) / 30

	return max(p,0)