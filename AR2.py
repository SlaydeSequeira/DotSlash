import os
import cvzone
import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector

# Initialize video capture to use the default camera
cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Setup for shirt and pants overlay

bannerPath = "C:/Users/SOHAM/OneDrive/Desktop/BNBFINAL/brocode/Resources/Shirts/7up.png"  # Ensure this is a PNG file


shirtRatioHeightWidth = 581 / 440
pantsNumber = 0

# Load the banner image with alpha channel support
imgBanner = cv2.imread(bannerPath, cv2.IMREAD_UNCHANGED)
if imgBanner is None:
    raise FileNotFoundError(f"Failed to load banner image: {bannerPath}")
if imgBanner.shape[2] != 4:  # Check if image has an alpha channel
    print(f"Warning: Banner image does not have an alpha channel: {bannerPath}")
    # Convert to 4 channels by adding an alpha channel
    b, g, r = cv2.split(imgBanner)
    alpha = np.ones(b.shape, dtype=b.dtype) * 255  # Full opacity
    imgBanner = cv2.merge((b, g, r, alpha))  # Add alpha channel


while True:
    success, img = cap.read()
    if not success:
        print("Failed to read camera frame")
        break

    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if bboxInfo:
        

        # Get face position for banner
        face_x = int(bboxInfo["bbox"][0])
        face_y = int(bboxInfo["bbox"][1])
        banner_width = 200  # Set the desired width for the banner
        banner_height = int(banner_width * imgBanner.shape[0] / imgBanner.shape[1])  # Maintain aspect ratio

        # Resize the banner
        imgBannerResized = cv2.resize(imgBanner, (banner_width, banner_height))

        # Position the banner beside the face
        banner_x = face_x + bboxInfo["bbox"][1]  # Place it to the right of the face
        banner_y = face_y  # Align it with the face vertically

        # Overlay the banner only if it has an alpha channel
        img = cvzone.overlayPNG(img, imgBannerResized, (banner_x, banner_y))

    cv2.imshow("Virtual Try-On", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()