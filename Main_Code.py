# ======================= Imported Libraries =======================
import cv2
import time
from time import sleep
import os
import datetime
from picamera2 import Picamera2
import pytesseract
import RPi.GPIO as GPIO
import sys
print(sys.executable)
# ======================= Button Configuration =======================
Mode_Btn = 40
Img_Capture_Btn = 38
Play_n_Pause = 36
Next_Page = 32
Prev_Page = 22
Next_PDF = 18
Prev_PDF = 16

def Configure_Button():
    GPIO.setup(Mode_Btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Img_Capture_Btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Play_n_Pause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Next_Page, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Prev_Page, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Next_PDF, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Prev_PDF, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# ======================= Camera Configuration =======================
def setup_camera():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1920, 1080)
    picam2.preview_configuration.sensor.output_size = (1920, 1080)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("video")
    picam2.start()
    return picam2

# ======================= Image Processing Functions =======================
def get_GrayScale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def remove_Noise(img):
    return cv2.medianBlur(img, 3)

def thresholding(img, limit):
    return cv2.threshold(img, limit, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)[1]

def thresholding_adaptive(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY_INV, 11, 2)

def sharpen_image(image):
    gaussian = cv2.GaussianBlur(image, (5, 5), 0)
    sharp = cv2.addWeighted(image, 3.5, gaussian, -2.5, -10)
    return sharp
# ======================= Read Text From PDF =======================
def extract_text_from_pdf(file_path, page_num=0):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        if page_num < len(pdf_reader.pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            return text
        else:
            return ""
# ======================= Motor Setup and Control =======================
motor1_pins = [7,11, 13, 15]
motor2_pins = [29, 31, 33, 35]

step_sequence = [
    [1,0,0,1],
    [1,0,0,0], 
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

def setup_motors():
    for pin in motor1_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def rotate_Motor(pins,steps,direction=1,delay=0.001):
    for _ in range(steps):
        steps_seq = step_sequence if direction == 1 else step_sequence[::-1]
        for step in steps_seq:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)
# ======================= Global Variables =======================
folder = "captured_images"
# 0 for Picture mode 1 for PDF mode 
Mode_Toggle = 1

# ======================= Auixilary Functions =======================
def Startup_Setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    setup_motors()
    Configure_Button()
    Add_Button_Events()
    folder = "captured_images"
    os.makedirs(folder, exist_ok=True)

def Image_Processing_Pipeline(frame):
    gray = get_GrayScale(frame)
    sharp = sharpen_image(gray)
    cv2.imwrite("GrayScale.jpg", gray)
    cv2.imwrite("Sharpened.jpg", sharp)

# ======================= Event Functions =======================   
def toggle_mode_Event(channel):
    global Mode_Toggle
    Mode_Toggle = 1 - Mode_Toggle

def Capture_image_Event(channel):
    if  Mode_Toggle == 0:
        picam2 = setup_camera()
        time.sleep(1)
        frame = picam2.capture_array()
        #cv2.imshow("Camera Feed", frame)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(folder, f"image_{timestamp}.jpg")
       # Image processing pipeline
        processed_Image = Image_Processing_Pipeline(frame)
        text = pytesseract.image_to_string(processed_Image)
        print("Detected Text:")
        print(text)
        print(f"Text Length: {len(text)}")
        picam2.stop()

def Play_n_Pause_Event(channel):
    print("PP")
def Next_Page_Event(channel):
    print("NPE") 
def Prev_Page_Event(channel):
    print("PPE") 
def Next_PDF_Event(channel):
    print("NextPDF") 
def Prev_PDF_Event(channel):
    print("PrevPDF")  

# Set up button interrupt for falling edge detection with debounce

def Add_Button_Events():
    GPIO.add_event_detect(Mode_Btn, GPIO.RISING, callback=toggle_mode_Event, bouncetime=300)
    GPIO.add_event_detect(Img_Capture_Btn, GPIO.RISING, callback=Capture_image_Event, bouncetime=300)
    GPIO.add_event_detect(Play_n_Pause, GPIO.RISING, callback=Play_n_Pause_Event, bouncetime=300)
    GPIO.add_event_detect(Next_Page, GPIO.RISING, callback=Next_Page_Event, bouncetime=300)
    GPIO.add_event_detect(Prev_Page, GPIO.RISING, callback=Prev_Page_Event, bouncetime=300)
    GPIO.add_event_detect(Next_PDF, GPIO.RISING, callback=Next_PDF_Event, bouncetime=300)
    GPIO.add_event_detect(Prev_PDF, GPIO.RISING, callback=Prev_PDF_Event, bouncetime=300)

def Picture_Mode():
    return

def PDF_Mode():
    print('PDF')

key ='d'
# ======================= Main OCR and Motor Control Routine =======================  
def main():
    Startup_Setup()
    #rotate_Motor(motor1_pins, 2048, direction=1)   # clockwise
    try:
        while True:
#             if GPIO.input(Mode_Btn) == GPIO.HIGH:
#                 if (Mode_Toggle == 1):
#                     Mode_Toggle =0
#                 else:
#                     Mode_Toggle = 1
#                 time.sleep(0.05)
                

            if key == ord('m'):
                print("Rotating motors...")
                
                print("Motors moved.")

            elif key == ord('q'):
                print("Exiting program...")
                break

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        GPIO.cleanup()
        cv2.destroyAllWindows()
        print("Camera stopped, motors cleaned up, and windows closed.")

# ======================= Program Entry Point =======================
if __name__ == "__main__":
    main()
