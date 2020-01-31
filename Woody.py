import cv2
import numpy

# import picamera
# import picamera.array
# from time import sleep
# import cv2

# import socket

# camera = picamera.PiCamera()


# camera.resolution = (320,240)
# rawCapture = picamera.array.PiRGBArray(camera,size=(320,240))

# s_v = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



# sleep(0.1)

# for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):
#     image = frame.array

#     result, imgencode = cv2.imencode('.jpg',image) 
    
#     cv2.imshow('frame',image)

#     s_v.sendto(imgencode, ("192.168.1.87", 9901))
    
#     rawCapture.truncate(0)
#     if cv2.waitKey(1) & 0xFF == ord('q'):s
#         break


cam1 = cv2.VideoCapture(0)

def webcam():
	ret1, img1 = cam1.read()
	if img1 != []:
		#print img1
		img1 = cv2.resize(img1,(320,240)) 
	#result, imgencode = cv2.imencode('.jpg',img1) 
	return img1
	#cv2.waitKey(10)



if __name__ == '__main__':
        while True:
                img = webcam()
                cv2.imshow('Frame', img)
                cv2.waitKey(10)
