import cv2
import numpy as np
import os
from tkinter import messagebox

def getAccountNumberFromFace(faceRecognizer):
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Press q to Quit", (450, 475), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), thickness=2)
        if (ret):
            faces = faceDetection(frame)
            if (len(faces) == 0):
                cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), thickness=2)
            elif (len(faces) >= 2):
                cv2.putText(frame, "Multiple faces detected Align Face Properly", (10, 50), cv2.FONT_HERSHEY_DUPLEX,
                            0.8, (0, 0, 255), thickness=2)
            else:
                for(x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
                    crop_img = frame[y:y + w, x:x + h]
                    cropGreyImg = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                    label,confidence = faceRecognizer.predict(cropGreyImg)
                    print(str(label)+"--"+str(confidence))
                    if (confidence > 60):
                        continue;
                    else:
                        cv2.destroyAllWindows()
                        cap.release()
                        return str(label)
            frame = cv2.resize(frame, (900, 700))

            cv2.imshow('Scanning Face', frame)
            cv2.setWindowProperty('Scanning Face', cv2.WND_PROP_TOPMOST, 1)


        if (cv2.waitKey(1) == ord('q')):
            cv2.destroyAllWindows()
            cap.release()
            return ""


def saveTrainedDataFile(self,faces, faceId):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceId))
    face_recognizer.save("trainingData.yml")
    self.controller.faceRecognizer=face_recognizer
    self.controller.ready=True
    cv2.destroyAllWindows()



def trainOurModel(self):
    faces,faceId=generateLabelsForTrainingData("data/")

    if(os.path.exists("trainingData.yml")):
        self.controller.ready=False
        os.remove("trainingData.yml")
        print("Hellofhdjfh")
    if(len(faces)>0):
        saveTrainedDataFile(self,faces,faceId)
    messagebox.showinfo("Model Updated","Successfully Trained Model")


def faceDetection(test_img):
    test_img = cv2.cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    face_haar_cascade = cv2.CascadeClassifier("View/haarcascade_frontalface_default.xml")
    faces = face_haar_cascade.detectMultiScale(test_img, scaleFactor=1.35, minNeighbors=5)
    return faces


def generateLabelsForTrainingData(directory):
    # this function goes to directory and save the subdirectory label and attach all the faces inside that subdirectory with the subdir name or callled label
    print("Generating labels for training...")
    faces = []
    faceId = []
    for (path, subdirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if filename[0:1]==".":
                print("Skipping System File")
            else:

                id = os.path.basename(path)
                img_path = os.path.join(path, filename)

                print(img_path, "--", id)
                test_img = cv2.imread(img_path)
                if test_img is None:
                    print("Image not loaded")
                    continue
                else:

                    facess = faceDetection(test_img)
                    if len(facess) != 1:
                        print("Two faces detected")
                    elif (len(facess) == 0):
                        print("No face found")
                    else:
                        x, y, w, h = facess[0]
                        roi_img = test_img[y:y + w, x:x + h]
                        roi_img=cv2.cvtColor(roi_img,cv2.COLOR_BGR2GRAY)
                        faces.append(roi_img)
                        faceId.append(int(id))
                        cv2.imshow('Training Model',roi_img)
                        cv2.setWindowProperty('Training Model', cv2.WND_PROP_TOPMOST, 1)
                        cv2.waitKey(1)

    return faces, faceId




def trainClassifier():
    # faces contains grey image having cropped face and faceId contains its label or id
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists("trainingData.yml")):
        print("Exits")
        face_recognizer.read("trainingData.yml")

    else:
        messagebox.showinfo("Wait","Wait for Model Training...")
        faces,faceId=generateLabelsForTrainingData("data/")
        if (len(faces))>0:
            face_recognizer.train(faces,np.array(faceId))
            face_recognizer.save("trainingData.yml")
            cv2.destroyAllWindows()
        else:
            cv2.destroyAllWindows()
            return face_recognizer,False

    return face_recognizer,True






def addFace(accNo):

    # Creating new Account
    if(os.path.exists("data/"+str(accNo))):
        print("Account Exists")
        print("Updating Face")
    else:
        print("Account Not exists So creating new Account")
        print("Adding Face")
        os.mkdir("data/"+str(accNo))


    # Detecting face
    cap = cv2.VideoCapture(0)
    count=0
    limit=50
    while (True):
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        # ret contains true or false......true if found any frame
        if (ret):
            faces = faceDetection(frame)
            if(len(faces)==0):
                cv2.putText(frame,"No Face Detected",(50,50),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,255),thickness=2)
            elif(len(faces)>=2):
                cv2.putText(frame,"Multiple faces detected Align Face Properly",(10,50),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,255),thickness=2)
            else:
                cv2.imwrite("data/" + accNo + "/" + str(count) + ".jpg", cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))

                cv2.putText(frame, "Writing image No. "+str(count+1), (10, 50), cv2.FONT_HERSHEY_DUPLEX,
                            0.8, (0, 255,0), thickness=2)

                count+=1
            frame=cv2.resize(frame,(900,700))


            cv2.imshow('Adding Face', frame)
            cv2.setWindowProperty('Adding Face', cv2.WND_PROP_TOPMOST, 1)

        if (cv2.waitKey(60) == ord('q')):
            break;
        if(count==limit):
            break;
    cv2.destroyAllWindows()
    cap.release()
