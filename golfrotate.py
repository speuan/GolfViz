import numpy as np
import cv2
import uuid

def rotate_image(image, angle):
  
  #rotates image
  
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def superimpose(background1, foreground1):
    
    #superimposes "foreground" on top of "background"
    
    # normalize alpha channels from 0-255 to 0-1
    alpha_background = background1[:,:,3] / 255.0
    alpha_foreground = foreground1[:,:,3] / 255.0

    # set adjusted colors
    background2=background1.copy()
    foreground2=foreground1.copy()

    for color in range(0, 3):
        background2[:,:,color] = alpha_foreground * foreground2[:,:,color] + \
            alpha_background * background2[:,:,color] * (1 - alpha_foreground)

    # set adjusted alpha and denormalize back to 0-255
    background2[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255 

    return background2



def translate(img,hor,vert):
    
    #shifts the img horizontally and vertically by "hor" and "vert" pixels
    #I think it doesn't wrap
    
    # The number of pixels
    num_rows, num_cols = img.shape[:2]

    # Creating a translation matrix
    translation_matrix = np.float32([ [1,0,hor], [0,1,vert] ])

    # Image translation
    img_translation = cv2.warpAffine(img, translation_matrix, (num_cols,num_rows))

    return img_translation


# Read in the background and foreground image
# foreground image can be transparent in parts
background = cv2.imread('15thScaled.png',-1)
foreground = cv2.imread('DistroScaled.png',-1)

#Prepare a viewing window (this enables stretching window)
cv2.namedWindow("output", cv2.WINDOW_NORMAL) 

#prepare initial iteration
newbackground = superimpose(background,foreground)
cv2.imshow('output',newbackground)

#the main lopp that waits for keyboard input and adjusts image accordingly
while(1):
    
    k = cv2.waitKey(0)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue

#rotation

    elif k==107:  #  "k" - rotate
        newforeground = rotate_image(foreground,1)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==108:  #  "l" - rotate
        newforeground = rotate_image(foreground,-1)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()

#small movements

    elif k==115:  #  "s" - move down
        newforeground = translate(foreground,0,5)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==97:  #  "a" - move left
        newforeground = translate(foreground,-5,0)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==100:  #  "d" - move right
        newforeground = translate(foreground,5,0)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==119:  #  "w" - move up
        newforeground = translate(foreground,0,-5)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy() 

#large movements

    elif k==103:  #  "g" - move down
        newforeground = translate(foreground,0,50)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==102:  #  "f" - move left
        newforeground = translate(foreground,-50,0)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==104:  #  "h" - move right
        newforeground = translate(foreground,50,0)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy()
    elif k==116:  #  "t" - move up
        newforeground = translate(foreground,0,-50)
        newbackground = superimpose(background,newforeground)
        cv2.imshow('output',newbackground)
        foreground = newforeground.copy() 

    elif k==112:  #  "p" - save image
        cv2.imwrite('%s.png'%(str(uuid.uuid1())),newbackground) 



    #else:
        #print(k)# else print its value  (Debug keys)

# cv2.destroyAllWindows() simply destroys all the windows we created.
cv2.destroyAllWindows()
 
