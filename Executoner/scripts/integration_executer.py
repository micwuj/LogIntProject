import cv2
import pytesseract
from subprocess import call

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def capture_screen():
    call(["adb", "shell", "screencap", "-p", "/sdcard/screen.png"])
    call(["adb", "pull", "/sdcard/screen.png", "screen.png"])
    return cv2.imread("screen.png")

def find_coordinates_of_screenshot(target_img_path, source_img):
    target_img = cv2.imread(target_img_path)
    result = cv2.matchTemplate(source_img, target_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc if max_val > 0.8 else None

def find_coordinates_of_text(text, source_img):
    gray_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(gray_img, config=custom_config, output_type=pytesseract.Output.DICT)
    text_coordinates = [(data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                        for i, t in enumerate(data['text']) if t.lower() == text.lower()]
    return text_coordinates

def tap(coordinates):
    if coordinates:
        x, y = coordinates
        call(["adb", "shell", "input", "tap", str(x), str(y)])

def type_in(coordinates, text):
    if coordinates:
        x, y = coordinates
        tap((x, y))  # Tap to focus the text field
        call(["adb", "shell", "input", "text", text])

def select(text):
    screenshot = capture_screen()
    text_coordinates = find_coordinates_of_text(text, screenshot)
    for coord in text_coordinates:
        tap((coord[0], coord[1]))
        break  # Assuming you just need the first occurrence

# Example usage:
screenshot = capture_screen()
coordinates = find_coordinates_of_screenshot('button.png', screenshot)
tap(coordinates)
