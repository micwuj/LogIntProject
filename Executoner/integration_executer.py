import cv2
import pytesseract
import json
import os
import time
from subprocess import call

# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR'

def install_app(apk_path):
    print("Installing APK:", apk_path)
    call(["adb", "-e", "install", apk_path])

def uninstall_app(package_name):
    print("Uninstalling app:", package_name)
    call(["adb", "-e", "uninstall", package_name])

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
        call(["adb", "shell", "input", "keyevent", "111"])

def monitor_folder(data_folder):
    current_files = set(os.listdir(data_folder))
    while True:
        time.sleep(1)
        new_files = set(os.listdir(data_folder))
        json_files = [f for f in new_files - current_files if f.endswith('.json')]

        for json_file in json_files:
            print(f"{json_file} is a new found file... working on it!")
            json_path = os.path.join(data_folder, json_file)
            with open(json_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    for item in entry:
                        print(item)    
                        if item['steps']:
                            install_app("./Executoner/apk_files/"+item['apk_file'])
                            for step in item['steps']:
                                print(step)
                                execute_step(step)
                            uninstall_app('com.example.dvs_driver_mirror')
            os.remove(json_path)
            current_files.update(json_files)

def execute_step(step):
    action = step['fields']['action']
    img_path = "/LogIntProject/media/" + step['fields']['img'] # poprawienie
    input_value = step['fields'].get('input_value', '')
    screenshot = capture_screen()
    
    if action == 'TYP':
        coordinates = find_coordinates_of_screenshot(img_path, screenshot)
        if coordinates:
            type_in(coordinates, input_value)
    elif action == 'TAP':
        coordinates = find_coordinates_of_screenshot(img_path, screenshot)
        if coordinates:
            tap(coordinates)

if __name__ == "__main__":
    data_folder = os.path.join(os.getcwd(), "Executoner/data")  # Folder do monitorowania
    monitor_folder(data_folder)
