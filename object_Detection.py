import cv2
import time

# define a list of objects of interest here
ooi = ['person', 'car', 'dog']

classNames = []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]

            # here we need to insert some lines of code
            if className in ooi:
                print('something')
            else:
                print('something else')

            objectInfo.append([box,className])
            if (draw):
                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    
    return img,objectInfo


if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    cap.set(3,640)
    cap.set(4,480)

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2)
        #print(objectInfo)
        cv2.imshow("Output",img)

        # break the loop if Esc is pressed
        if cv2.waitKey(1) == ord(" "):
            break