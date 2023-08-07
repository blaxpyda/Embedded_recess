import cv2
import pytesseract
import serial
import numpy as np

# Set the Tesseract executable path 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open the serial connection
ser = serial.Serial('COM5', 9600)

# Function to read an image from the serial connection
def read_image():
    data = []
    for i in range(240): # height of the image
        row = []
        for j in range(320): # width of the image
            byte = ser.read()
            row.append(int.from_bytes(byte, byteorder='big'))
        data.append(row)
    img = np.array(data, dtype=np.uint8)
    return img

#call read image function to get image from the serial port
img = read_image()

#showing the image
cv2.imshow("original image", img)
cv2.waitKey(0)

#reducing the noise in the greyscale image
gray_image = cv2.bilateralFilter(img, 11, 17, 17) 
cv2.imshow("smoothened image", gray_image)
cv2.waitKey(0)

#Detecting edges
edged = cv2.Canny(gray_image, 30, 200) 
cv2.imshow("edged image", edged)
cv2.waitKey(0)

#Contours from the edged image onto the original image 
cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=img.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("contours",image1)
cv2.waitKey(0)

#sorting the contours
cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = img.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 contours",image2)
cv2.waitKey(0)

#Finding the contour with 4 sides
i=7
for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4: 
                screenCnt = approx

#cropping rectangular part identified as license plate
                x,y,w,h = cv2.boundingRect(c) 
                new_img=img[y:y+h,x:x+w]
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", img)
cv2.waitKey(0)

#Extracting text from the cropped plate
Cropped_loc = './7.png'
cv2.imshow("cropped", cv2.imread(Cropped_loc))
plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
print("Number plate is:", plate)
cv2.waitKey(0)
cv2.destroyAllWindows()