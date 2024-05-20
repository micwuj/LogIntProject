#!/bin/bash

adb -e install ./app-debug.apk
adb shell monkey -p com.example.loginttester2 1

adb shell input tap 600 600
adb shell input text "JohnDoe123"

adb shell input tap 600 800
adb shell input text "Package404"

adb shell input tap 600 1000
adb shell input text "Loaded"

adb shell input tap 600 1200
adb shell input text "24.05.2024:13:00"

adb shell input keyevent 4


adb shell input tap 100 1450
sleep 1
adb shell input tap 600 1440

# echo "Press Enter to uninstall app and end script"
# read
sleep 1
adb -e uninstall com.example.loginttester2
