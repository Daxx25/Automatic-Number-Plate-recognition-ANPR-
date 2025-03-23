import cv2
import os


def splitvedio(vediopath,src,data_dir):
    # Read the video from specified path
    os.chdir(src)
    # print(vediopath+' ...splitfunction vedio path')
    cam = cv2.VideoCapture(vediopath)
      
    os.chdir(src)
    currentframe = 0
    ret = True
    while(True):
          
        # reading from frame
        ret,frame = cam.read()

        if not ret:
            break
      
        if ret:
            # if video is still left continue creating images
            name = os.path.join(data_dir,'frame_'+str(currentframe) + '_.jpg')
            # name = './data/frames' + str(currentframe) + '.jpg'
            print ('Creating...' + name)
      
            # writing the extracted images
            cv2.imwrite(name, frame)
      
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break
      
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return 'successfully created frames of the input vedio'