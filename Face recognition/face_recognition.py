#Recognize faces using some classification algorithm - like logistic, knn, svm. 
#here we will use KNN algorithm
'''
1. load training data(numpy arrays of all the personss)
  x-values are stored in the numpy arrays
  y-values we need to assign for each person
  2. read a video stream using openCv
  3. extract faces out of it 
  4.use knn to find the prediction of face (int)
  5. map the predicted id to name of user
  6. display the predictions on the screen / bounding box and name
  
'''

import cv2
import numpy as np
import os

#KNN code 
def distance(v1, v2):
    return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):
    dist = []
    
    for i in range(train.shape[0]):
        #get vector and label
        ix = train[1, :-1]
        iy = train[1, -1]
        #compute the distance from test point 
        d = distance(test, ix)
        dist.append([d,iy])
        
    #Sort based on distance and get top k
    dk = sorted(dist, key=lambda x: x[0])[:k]
    #Retrieve only the labels
    labels = np.array(dk)[:, -1]
    
    #get frequencies of each label 
    output = np.unique(labels, return_counts=True)
    #Find max frequency and corresponding label
    index = np.argmax(output[1])
    return output[0][index]

#-------------------------------------
#init web cam
cap = cv2.VideoCapture(0)

#Face detection 
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

#data preparartion 
class_id = 0 #labels for given file
names = {} #mapping id with name
dataset_path="./data/"

face_data = []
labels = []

for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        
        #create a mapping btw class_id and name 
        names[class_id] = fx[:-4]
        
        data_item = np.load(dataset_path+fx)
        face_data.append(data_item)
        
        #create labels for class
        target = class_id * np.ones((data_item.shape[0], ))
        class_id+=1
        labels.append(target)

face_dataset = np.concatenate(face_data, axis = 0)
face_labels = np.concatenate(labels, axis=0).reshape((-1,1))
        
train_set = np.concatenate((face_dataset, face_labels), axis=1)    
print(train_set.shape)  


# TESTING 

while True:
    ret, frame = cap.read()
    
    if ret==False:
        continue
    
    
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
    #1.3 is scaling factor  - read doc openCv frontal face detection how haarcascade classifier works
    if len(faces)==0:
        continue
    
    #pick the last face as it has largest area
    for face in faces:
        #draw bounding box or the rectangle
        
        x,y,w,h = face
        
        #extract crop out required face : region of interest ----in gray scale first write y axis, then x axis
        offset = 10
        face_section = gray_frame[y-offset:y+h+offset, x-offset:x+w+offset]
        face_section = cv2.resize(face_section,(100,100))
        
        #PREDICT 
        out = knn(train_set, face_section.flatten())
        
        #display output on screen
        pred_name = names[int(out)]
        cv2.putText(gray_frame,pred_name, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX , 1 , (255, 0, 0), 2 , cv2.LINE_AA)
        
        cv2.rectangle(gray_frame, (x,y), (x+w,y+h),(0, 255, 255) , 2)
        #           start coordinate  end cordinate, color, thickness
    
   # cv2.imshow("Frame", frame)
    cv2.imshow("gray_frame", gray_frame)
    
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):  #ord gives ascii value
        break

cap.release()
cv2.destroyAllWindows()
        