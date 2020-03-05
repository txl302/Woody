import itertools
import numpy
import math
import time

from math import *

import pypot.dynamixel

ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)  

if not ports:
    raise IOError('No port available.') 

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

found_ids = dxl_io.scan(range(13))
print('Found ids:', found_ids)

if len(found_ids) < 2:
    raise IOError('You should connect at least two motors on the bus for this test.')
#chose all motors and enable torque and set the same speed
ids = found_ids[:]
#dxl_io.enable_torque(ids)
    
#def move_to(m_id, speed, pose):
def move_to(m_id, pose):
    #dxl_io.set_moving_speed(dict(zip(m_id, itertools.repeat(speed))))
    dxl_io.set_goal_position(dict(zip(m_id, pose)))

def get_present_position(m_id):
    p = dxl_io.get_present_position(m_id)
    return p

def Guss(mu, sigma, x):
	f = 1/(sqrt(2*pi)*sigma)*pow(e, (-pow((x - mu), 2)/(2*pow(sigma,2))))
	return f

def run_guss(m_id, current_pos, des_pos, time_inv):
	current_time = time.time()
	des_time  = current_time + time_inv
	n = len(m_id)

	while True:
		if time.time() <= des_time:
			speed = []
			pose = []
			for i in range(n):
				speed.append((des_pos[i] - current_pos[i])*Guss(current_time, 1, time.time() - time_inv/2))
				pose.append(current_pos[i] + (des_pos[i] - current_pos[i])*(time.time() - current_time)/(des_time - current_time))
			#move_to(m_id, pose, speed)
			print(pose, speed)
		else:
			break


def run_tri(m_id, current_pos, des_pos, time_inv):
	current_time = time.time()
	des_time  = current_time + time_inv
	n = len(m_id)
	time_tmp = time.time()

	pose = current_pos

	v_top = []
	k =[]

	#print(des_pos, current_pos)

	for i in range(n):
		v_top.append(2*(des_pos[i] - current_pos[i])/time_inv)
		
	for i in range(n):
		k.append(v_top[i]*2/time_inv)




	while time.time()<= des_time:
		time_slot = time.time() - time_tmp
		time_tmp = time.time()



		if time_tmp <= current_time + time_inv/2:
			speed = []
			for i in range(n):
				speed.append(k[i]*(time_tmp - current_time))
			for i in range(n):
				pose[i] += speed[i]*time_slot


		elif (time_tmp >= current_time + time_inv/2) & (time_tmp <= des_time):
			speed = []
			for i in range(n):
				speed.append(k[i]*(des_time - time_tmp))
			for i in range(n):
				pose[i] += speed[i]*time_slot

		#print(pose)
		#move_to(m_id, pose, speed)

	

pos1 = [1.32, -1.83]
pos2 = [-86.07, 87.54]

ids = [3, 8]


if __name__ == '__main__':
	while True:
		run_tri(ids, pos1, pos2, 6)
		time.sleep(3)
		print(pos1, pos2)
		run_tri(ids, pos2, pos1, 6)
		time.sleep(3)
		print(pos1, pos2)
