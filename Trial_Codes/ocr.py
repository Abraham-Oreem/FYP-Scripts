import cv2
import pytesseract
from time import sleep

def TakeImage():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'): 
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                webcam.release()
                print("Image saved!")
                break
        
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break
    
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    return frame
def OCR_Core(img):
    text = pytesseract.image_to_string(img)
    return text

def get_GrayScale(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def remove_Noise(img):
    return cv2.medianBlur(img,3)

def thresholding(img):
    return cv2.threshold(img,128,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)[1]

def thresholding1(img):
    # Adaptive thresholding for better binarization
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 2)
    return img

def upscale_image(img, scale=2):
    return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
def main():
    #TakeImage()
    image = cv2.imread('C:/Users/Dell/Desktop/FYP/Code/this.jpg')
    #image = upscale_image(image, scale=2)
    #cv2.imwrite('Upscaled.jpg', image)
    image = get_GrayScale(image)
    cv2.imwrite(filename='GrayScale.jpg', img=image)
    image = thresholding(image)
    cv2.imwrite(filename='Thresh.jpg', img=image)
    image = remove_Noise(image)
    cv2.imwrite(filename='Smooth.jpg', img=image)
    text=OCR_Core(image)
    print(text)
    print(len(text))
    
if __name__ == "__main__":
    main()