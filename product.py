import cv2
import numpy as np
import os
import time
import gui
from PIL import Image
import pyperclip
import char_detection
import plate_detection
import total_plate
import sqlite3
from sqlite3 import Error
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)
showSteps = False
def database1(image_path,src):
    os.chdir(src)
    conn = sqlite3.connect('database.db')
    c1=conn.cursor()
    img_path = image_path
    lic = main(img_path)
    # c1.execute('SELECT * FROM number_plate where plate_number=?',(lic,))
    # r=c1.fetchone()
    # if(r!=None):
    #     print("Number Plate Detected")
    #     print("The details of the Car Owner are as follows:")
    #     print("1. Number_Plate = " +r[0])
    #     print("2. Name Of the Car Owner : " +r[1])
    #     print("3. Phone_number : " +str(r[2]))
    #     print("4. Address : " +r[3])
    # else:
    #     print("Unauthorized vehicle")
    return lic

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0
    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0
    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0
    intFontThickness = int(round(fltFontScale * 1.5))
    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene
    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)
    ptCenterOfTextAreaX = int(intPlateCenterX)
    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))
    textSizeWidth, textSizeHeight = textSize
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)

def main(img_path):
    blnKNNTrainingSuccessful = char_detection.loadKNNDataAndTrainKNN()
    if blnKNNTrainingSuccessful == False:
        print("\nerror: KNN traning was not successful\n")
        return
    # imgOriginalScene  = cv2.imread(pyperclip.paste())
    imgOriginalScene  = cv2.imread(img_path)
    
    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return
    listOfPossiblePlates = plate_detection.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = char_detection.detectCharsInPlates(listOfPossiblePlates)
    cv2.imshow("imgOriginalScene", imgOriginalScene)
    if len(listOfPossiblePlates) == 0:
        print("\nno license plates were detected\n")
    else:
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        licPlate = listOfPossiblePlates[0]
        cv2.imshow("imgPlate", licPlate.imgPlate)
        cv2.imshow("imgThresh", licPlate.imgThresh)
        py_dir = os.getcwd()
        directory = "scanned_plates"
        path = os.path.join(py_dir, directory)
        
        number = str(int(len(os.listdir(os.getcwd()))/3))
        # cv2.imwrite("imgPlate" + number + ".png", licPlate.imgPlate)
        # cv2.imwrite("imgThresh" + number + ".png", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return
        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)
        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")
        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

        os.chdir(path)
        cv2.imshow("imgOriginalScene", imgOriginalScene)
        cv2.imwrite("imgOriginalScene_" + number + ".png", imgOriginalScene)
        cv2.imwrite("imgPlate_" + number + "_.png", licPlate.imgPlate)
        cv2.imwrite("imgThresh_" + number + "_.png", licPlate.imgThresh)
        os.chdir(py_dir)
    # cv2.waitKey(0)
    return(licPlate.strChars)

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
