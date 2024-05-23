#!/bin/bash

# Ścieżka do pliku .json
CWD=$(pwd)
JSON_FILE="tmp_data.json"

USERNAME=$(jq -r '.id' $JSON_FILE)
PASSWORD=$(jq -r '.assignment_id' $JSON_FILE)
STATUS=$(jq -r '.type' $JSON_FILE)
DATETIME=$(jq -r '.created_at' $JSON_FILE)


adb -e install ../apk_files/app-debug.apk
adb shell monkey -p com.example.loginttester2 1

adb shell input tap 600 700
adb shell input text $USERNAME

adb shell input tap 600 935
adb shell input text $PASSWORD

adb shell input tap 600 1170
adb shell input text $STATUS

adb shell input tap 600 1400
adb shell input text $DATETIME

adb shell input keyevent 4

adb shell input tap 100 1450
sleep 2
adb shell input tap 600 1650

sleep 3
adb -e uninstall com.example.loginttester2
