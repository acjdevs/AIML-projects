#write python script that captures images from your webcam video stream
# extracts all faces from the images frame using haarcascades
#stores fsce information into numpy arrays
'''
1. read and show video stream, capture images
2. detect faces and show bounding box haarcascades
3. flatten largest face image(gray scale) and save in a  numpy array
4. repeat the above for multiple people to generate training data
'''
import cv2
import numpy as np

#init web cam
cap = cv2.VideoCapture(0)

#Face detection 
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

face_data = []
dataset_path = "./data/"
file_name = input("Enter the name of the person :")


while True:
    ret, frame = cap.read()
    
    if ret==False:
        continue
    
    
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
    #1.3 is scaling factor  - read doc openCv frontal face detection how haarcascade classifier works
    if len(faces)==0:
        continue
    
    faces = sorted(faces, key=lambda f:f[2]*f[3])
    #pick the last face as it has largest area
    for face in faces[-1:]:
        #draw bounding box or the rectangle
        
        x,y,w,h = face
        cv2.rectangle(gray_frame, (x,y), (x+w,y+h),(0, 255, 255) , 2)
        #           start coordinate  end cordinate, color, thickness

        #extract crop out required face : region of interest ----in gray scale first write y axis, then x axis
        offset = 10
        face_section = gray_frame[y-offset:y+h+offset, x-offset:x+w+offset]
        face_section = cv2.resize(face_section, (100,100))
        face_data.append(face_section)
        print(len(face_section))
    
   # cv2.imshow("Frame", frame)
    cv2.imshow("gray_frame", gray_frame)
    
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):  #ord gives ascii value
        break
    
#convert face data list to numpy array (so use .npy )
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))   #rows,col
print(face_data.shape)
    
#save this data into  file system
np.save(dataset_path+file_name+'.npy', face_data)
print("Data Saved Successfully!!! : ")
    
cap.release()
cv2.destroyAllWindows()
    
