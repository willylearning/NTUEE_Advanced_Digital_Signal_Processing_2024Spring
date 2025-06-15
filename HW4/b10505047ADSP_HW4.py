import numpy as np
import cv2

# please enter the input image x and y here ( will be changed to grayscale )
img_x = cv2.imread("imagex.jpg", cv2.IMREAD_GRAYSCALE) # enter the input image x here, ex:Baboon.jpg
img_y = cv2.imread("imagey.jpg", cv2.IMREAD_GRAYSCALE) # enter the input image y here, ex:Peppers.jpg

means_x = np.mean(img_x) # means of x
means_y = np.mean(img_y) # means of y

var_x = np.mean((img_x-means_x)**2) # variance of x
var_y = np.mean((img_y-means_y)**2) # variance of y
corvar_xy = np.mean((img_x-means_x)*(img_y-means_y)) # covariance of x and y

c1, c2 = (1/255)**0.5, (1/255)**0.5 # adjustable constant

L = 255 # the maximal possible value of x - the minimal possible value of x

# ssim calculation
ssim = ((2*means_x*means_y + (c1*L)**2)*(2*corvar_xy + (c2*L)**2))/((means_x**2 + means_y**2 + (c1*L)**2)*(var_x + var_y + (c2*L)**2))

print("ssim of image x and y is ", ssim)