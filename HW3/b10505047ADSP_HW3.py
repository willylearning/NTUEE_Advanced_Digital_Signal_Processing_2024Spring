import numpy as np
from PIL import Image

# img = Image.open('Baboon1.bmp')
img = Image.open('pictureA.jpg') # please enter the input picture A here
(w, h) = img.size # w is horizontal, h is vertical
# print(w, h)
R_1d = np.array(img.getdata(band = 0 ))
G_1d = np.array(img.getdata(band = 1 ))
B_1d = np.array(img.getdata(band = 2 ))

# 1d array to h x w array
R = R_1d.reshape((h,w))
G = G_1d.reshape((h,w))
B = B_1d.reshape((h,w))

# convert RGB to YCbCr
Y = 0.299*R + 0.587*G + 0.114*B
Cb = -0.169*R - 0.331*G + 0.5*B
Cr = 0.5*R - 0.419*G - 0.081*B

# downsampling
Cb1 = np.zeros((h//2, w//2)) # Cb1 is Cb after 4:2:0
Cr1 = np.zeros((h//2, w//2)) # Cr1 is Cr after 4:2:0
for m in range(h//2):
    for n in range(w//2):
        Cb1[m, n] = Cb[2*m, 2*n]
        Cr1[m, n] = Cr[2*m, 2*n]

# recover
Cb_inv = np.zeros((h, w)) # we want to recover Cb1 -> Cb_inv
Cr_inv = np.zeros((h, w)) # we want to recover Cr1 -> Cr_inv

# interpolation
for m in range((h//2)):
    for n in range((w//2)):
        Cb_inv[2*m, 2*n] = Cb1[m, n]
        Cr_inv[2*m, 2*n] = Cr1[m, n]
        
for m in range((h//2)-1):
    for n in range((w//2)-1):
        Cb_inv[2*m, 2*n+1] = ((Cb_inv[2*m, 2*n] + Cb_inv[2*m, 2*n+2])/2)
        Cr_inv[2*m, 2*n+1] = ((Cr_inv[2*m, 2*n] + Cr_inv[2*m, 2*n+2])/2)

for m in range((h//2)-1):
    for n in range(w):
        Cb_inv[2*m+1, n] = ((Cb_inv[2*m, n] + Cb_inv[2*m+2, n])/2)
        Cr_inv[2*m+1, n] = ((Cr_inv[2*m, n] + Cr_inv[2*m+2, n])/2)

# deal with the last row and column
for m in range(h):
    Cb_inv[m, w-1] = Cb_inv[m, w-2] # last column
for n in range(w):
    Cb_inv[h-1, n] = Cb_inv[h-2, n] # last row

# YCbCr back to RGB
R_inv = Y-0.00092*(Cb_inv)+1.40169*(Cr_inv)
G_inv = Y-0.343695*(Cb_inv)-0.714169*(Cr_inv)
B_inv = Y+1.77216*(Cb_inv)+0.00099*(Cr_inv)

# make sure R,G,B in [0,255]
R_inv = (np.clip(R_inv, 0, 255)).astype(int)
G_inv = (np.clip(G_inv, 0, 255)).astype(int)
B_inv = (np.clip(B_inv, 0, 255)).astype(int)

image_RGB_inv = np.dstack((R_inv,G_inv,B_inv))
image_inv = Image.fromarray(image_RGB_inv.astype('uint8')).convert('RGB')
image_inv.save('pictureB.jpg')