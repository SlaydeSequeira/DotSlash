import os
import cvzone
import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector

# Initialize video capture to use the default camera
cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Setup for shirt and pants overlay
shirtFolderPath = "Resources/Shirts"
pantsFolderPath = "Resources/Pants"
listShirts = os.listdir(shirtFolderPath)
listPants = os.listdir(pantsFolderPath)
shirtRatioHeightWidth = 581 / 440
pantsNumber = 0

def get_shirt_coordinates(img, bboxInfo):
    """Calculate shirt coordinates based on the person's bounding box"""
    bbox = bboxInfo["bbox"]
    center = bboxInfo["center"]

    shirt_width = int(bbox[2] * 0.8)  # 80% of person's width
    shirt_height = int(shirt_width * shirtRatioHeightWidth)

    x1 = max(0, center[0] - shirt_width // 2)
    y1 = max(0, bbox[1] + bbox[3] // 6)  # Start from 1/6th of the body height

    return x1, y1, shirt_width, shirt_height

def get_pants_coordinates(img, bboxInfo, shirt_width):
    """Calculate pants coordinates based on the person's bounding box and adjust to fit shirt width"""
    bbox = bboxInfo["bbox"]
    center = bboxInfo["center"]

    # Stretch pants horizontally to be 2/3 of the shirt width
    pants_width = int(shirt_width * 1.5)  # Make the pants wider relative to the shirt
    pants_height = int(pants_width * (3 / 2))  # Adjust the height ratio

    x1 = max(0, center[0] - pants_width // 2)
    # Adjusted to start lower down the body
    y1 = max(0, bbox[1] + int(bbox[3] * 0.5))  # Start from halfway down the body

    return x1, y1, pants_width, pants_height

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read camera frame")
        break

    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if bboxInfo:
        # Process shirt
        x1_shirt, y1_shirt, shirt_width, shirt_height = get_shirt_coordinates(img, bboxInfo)
        try:
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[0]), cv2.IMREAD_UNCHANGED)
            if imgShirt is None:
                raise FileNotFoundError(f"Failed to load shirt image: {listShirts[0]}")
            imgShirt = cv2.resize(imgShirt, (shirt_width, shirt_height))
            img = cvzone.overlayPNG(img, imgShirt, (x1_shirt, y1_shirt))
        except Exception as e:
            print(f"Error processing shirt overlay: {e}")

        # Process pants
        x1_pants, y1_pants, pants_width, pants_height = get_pants_coordinates(img, bboxInfo, shirt_width)
        try:
            imgPants = cv2.imread(os.path.join(pantsFolderPath, listPants[pantsNumber]), cv2.IMREAD_UNCHANGED)
            if imgPants is None:
                raise FileNotFoundError(f"Failed to load pants image: {listPants[pantsNumber]}")
            imgPants = cv2.resize(imgPants, (pants_width, pants_height))
            img = cvzone.overlayPNG(img, imgPants, (x1_pants, y1_pants))
        except Exception as e:
            print(f"Error processing pants overlay: {e}")

    cv2.imshow("Virtual Try-On", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
