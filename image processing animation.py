# importing libraries 
import os
import cv2
import numpy as np

# Checking the current directory path 
print(os.getcwd())

# Folder which contains all the images 
# from which video is to be generated
pa=input("enter the path of image folder:")
os.chdir(pa)
path = pa

mean_height = 0
mean_width = 0

num_of_images = len(os.listdir('.'))

for file in os.listdir('.'):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        im = cv2.imread(os.path.join(path, file))
        width, height = im.shape[0:2]
        mean_width += width
        mean_height += height
    #im.show() # uncomment this for displaying the image

# Finding the mean height and width of all images. 
# This is required because the video frame needs 
# to be set with same width and height. Otherwise 
# images not equal to that width height will not get 
# embedded into the video 
mean_width = int(mean_width / (num_of_images))
mean_height = int(mean_height / (num_of_images))


# Resizing of the images to give 
# them same width and height
print("RESIZING YOUR IMAGES....\n")
i=1

for file in os.listdir('.'):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        
        im = cv2.imread(os.path.join(path, file))
        
        #time.sleep(.5)
        print("{:.2f}% COMPLETE.........".format(100*i/num_of_images),end='\r')
        i=i+1
        #resizing
        imResize = cv2.resize(im,(mean_height,mean_width ))
        cv2.imwrite(os.path.join(path, file) ,imResize) # setting quality 
        
print("RESIZING OF IMAGES COMPLETE:)")


# Video Generating function
def generate_video():
    image_folder = '.'
    f=int(input("ENTER THE FRAME RATE (FPS)"))
    video_name = input("\nENTER NAME OF YOUR VIDEO..")+'.avi'
    os.chdir(pa)

    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]

    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape
    print("NOW MAKING YOUR VIDEO HAVE PATIENCE:\n")
    video = cv2.VideoWriter(video_name, 0, f, (width, height))

    # Appending the images to the video one by one
    i=1
    l=len(images)
    for image in images:
        tim=(cv2.imread(os.path.join(image_folder, image)))
        for x in range(2*f):
            video.write(tim)
        if i<l:
            tim2=(cv2.imread(os.path.join(image_folder, images[i])))
            r=360/f;
            j=r
            
            for z in np.linspace(0, 1, f):
                alpha = z
                beta = 1 - alpha
                output = cv2.addWeighted(tim2, alpha, tim, beta, 0)
                (row,col)=output.shape[0:2]
                m=cv2.getRotationMatrix2D((col / 2, row / 2), j, 1)
                res = cv2.warpAffine(output, m, (col, row)) 
                video.write(res)
                j=j+r
            i=i+1
        
        print("{:.2f}% COMPLETE............".format(100*i/l),end='\r')
        

    print('\nYOUR VIDEO MAKING IS COMPLETE ENJOY :)')
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated


# Calling the generate_video function 
generate_video() 
