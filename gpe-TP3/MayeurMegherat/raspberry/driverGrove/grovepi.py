import sys
import time
import math
import struct
import numpy

debug = 0

if sys.version_info<(3,0):
	p_version=2
else:
	p_version=3

if sys.platform == 'uwp':
	import winrt_smbus as smbus
	bus = smbus.SMBus(1)
else:
	import smbus
	import RPi.GPIO as GPIO
	rev = GPIO.RPI_REVISION
	if rev == 2 or rev == 3:
		bus = smbus.SMBus(1)
	else:
		bus = smbus.SMBus(0)

# I2C Address of Arduino
address = 0x04

# Command Format
# digitalRead() command format header
dRead_cmd = [1]
# digitalWrite() command format header
dWrite_cmd = [2]
# analogRead() command format header
aRead_cmd = [3]
# analogWrite() command format header
aWrite_cmd = [4]
# pinMode() command format header
pMode_cmd = [5]
# Ultrasonic read
uRead_cmd = [7]
# Get firmware version
version_cmd = [8]

# This allows us to be more specific about which commands contain unused bytes
unused = 0
retries = 10
# Function declarations of the various functions used for encoding and sending
# data from RPi to Arduino


# Write I2C block
def write_i2c_block(address, block):
	for i in range(retries):
		try:
			return bus.write_i2c_block_data(address, 1, block)
		except IOError:
			if debug:
				print ("IOError")
	return -1

# Read I2C byte
def read_i2c_byte(address):
	for i in range(retries):
		try:
			return bus.read_byte(address)
		except IOError:
			if debug:
				print ("IOError")
	return -1


# Read I2C block
def read_i2c_block(address):
	for i in range(retries):
		try:
			return bus.read_i2c_block_data(address, 1)
		except IOError:
			if debug:
				print ("IOError")
	return -1

# Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address, dRead_cmd + [pin, unused, unused])
	# time.sleep(.1)
	n = read_i2c_byte(address)
	return n

# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, dWrite_cmd + [pin, value, unused])
	return 1


# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	if mode == "OUTPUT":
		write_i2c_block(address, pMode_cmd + [pin, 1, unused])
	elif mode == "INPUT":
		write_i2c_block(address, pMode_cmd + [pin, 0, unused])
	return 1


# Read analog value from Pin
def analogRead(pin):
	write_i2c_block(address, aRead_cmd + [pin, unused, unused])
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return number[1] * 256 + number[2]


# Write PWM
def analogWrite(pin, value):
	write_i2c_block(address, aWrite_cmd + [pin, value, unused])
	return 1


# Read value from Grove Ultrasonic
def ultrasonicRead(pin):
	write_i2c_block(address, uRead_cmd + [pin, unused, unused])
	time.sleep(.06)	#firmware has a time of 50ms so wait for more than that
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return (number[1] * 256 + number[2])
