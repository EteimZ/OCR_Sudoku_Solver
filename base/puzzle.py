#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 04:37:40 2021

@author: eteims
"""

# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
from PIL import Image
import os
import cv2
import glob

def find_puzzle(image):
	# convert the image to grayscale and blur it slightly
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    
	# apply adaptive thresholding and then invert the threshold map
	thresh = cv2.adaptiveThreshold(blurred, 255,
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	thresh = cv2.bitwise_not(thresh)
	# check to see if we are visualizing each step of the image
	# processing pipeline (in this case, thresholding)
	
	# Store and convert threshhold image
	imageConverter(thresh, "app/static/Threshold.png")

        
	# find contours in the thresholded image and sort them by size in
	# descending order
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	# initialize a contour that corresponds to the puzzle outline
	puzzleCnt = None
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we can
		# assume we have found the outline of the puzzle
		if len(approx) == 4:
			puzzleCnt = approx
			break
        
	# if the puzzle contour is empty then our script could not find
	# the outline of the Sudoku puzzle so raise an error
	if puzzleCnt is None:
		raise Exception(("Could not find Sudoku puzzle outline. "
			"Try debugging your thresholding and contour steps."))
	# check to see if we are visualizing the outline of the detected
	# Sudoku puzzle

	# draw the contour of the puzzle on the image and then display
	# it to our screen for visualization/debugging purposes
	output = image.copy()
	cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
	imageConverter(output, "app/static/outline.png")

        
	# apply a four point perspective transform to both the original
	# image and grayscale image to obtain a top-down bird's eye view
	# of the puzzle
	puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
	warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))
	# check to see if we are visualizing the perspective transform
	
	imageConverter(puzzle, "app/static/transform.png")

	# return a 2-tuple of puzzle in both RGB and grayscale
	return (puzzle, warped)

def extract_digit(cell):
	
    # apply automatic thresholding to the cell and then clear any
	# connected borders that touch the border of the cell
	thresh = cv2.threshold(cell, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = clear_border(thresh)
	
    # check to see if we are visualizing the cell thresholding step

	imageConverter(thresh, "app/static/thresh.png")

        
	# find contours in the thresholded cell
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
    
	# if no contours were found than this is an empty cell
	if len(cnts) == 0:
		return None
    
	# otherwise, find the largest contour in the cell and create a
	# mask for the contour
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
    
    # compute the percentage of masked pixels relative to the total
	# area of the image
	(h, w) = thresh.shape
	percentFilled = cv2.countNonZero(mask) / float(w * h)
    
	# if less than 3% of the mask is filled then we are looking at
	# noise and can safely ignore the contour
	if percentFilled < 0.03:
		return None
    
	# apply the mask to the thresholded cell
	digit = cv2.bitwise_and(thresh, thresh, mask=mask)
		
    # return the digit to the calling function
	return digit

# Function to convert image and save iamge 
def imageConverter(image, path):
	if os.path.exists(path):																									
		os.remove(path)
	PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
	PIL_image.save(path)

# Function to delete all images in digits
def deleteDigit(path):
	# Use glob module to grab files pathern 
	files = glob.glob(path + '/*')
	
	if files != []:
		# Interate over files
		for file in files:
			os.remove(file)
	else:
		pass