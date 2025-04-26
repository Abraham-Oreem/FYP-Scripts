import cv2
import pytesseract
from time import sleep

def TakeImage():
    key = cv2.waitKey(1)
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

        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off. Program ended.")
            cv2.destroyAllWindows()
            break
            
    return frame

def OCR_Core(img):
    text = pytesseract.image_to_string(img)
    return text

def get_GrayScale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def remove_Noise(img):
    return cv2.GaussianBlur(img, (5, 5), 0)  # Gaussian blur for noise removal

def thresholding(img):
    # Adaptive thresholding for better binarization
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 2)
    return img

def invert_image(img):
    return cv2.bitwise_not(img)  # Inverts black ↔ white

def main():
    image = TakeImage()  # Uncomment if you want to capture an image using the webcam
    image = cv2.imread('C:/Users/Dell/Desktop/FYP/Code/saved_img.jpg')

    image = get_GrayScale(image)
    cv2.imwrite('GrayScale.jpg', image)

    image = thresholding(image)
    cv2.imwrite('Thresh.jpg', image)
    # image = invert_image(image)  # Ensure white text on dark background is processed
    # cv2.imwrite('Inverted.jpg', image)

    image = remove_Noise(image)
    cv2.imwrite('Smooth.jpg', image)

    text = OCR_Core(image)
    print("Extracted Text:\n", text)
    print("Character Count:", len(text))

if __name__ == "__main__":
    main()
