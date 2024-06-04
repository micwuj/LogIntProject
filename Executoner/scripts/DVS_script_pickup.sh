#!/bin/bash

# Ścieżka do pliku .json
CWD=$(pwd)
JSON_FILE="tmp_data.json"
# USERNAME=$(jq -r '.id' $JSON_FILE)
# PASSWORD=$(jq -r '.assignment_id' $JSON_FILE)

USER="1"
PASSWORD="1"
TRANSPORT_ID="1412331"

adb -e install ../apk_files/dvs_driver_mirror.apk
adb shell monkey -p com.example.dvs_driver_mirror 1

adb shell input tap 500 1500
adb shell input text $USER

adb shell input tap 500 1800
adb shell input text $PASSWORD

adb shell input keyevent 4
sleep 2
adb shell input tap 1000 2100
sleep 2
adb shell input tap 500 1500

sleep 2
adb shell input tap 500 1500
adb shell input text $TRANSPORT_ID
adb shell input tap 1000 1740

sleep 2
adb shell input tap 200 1200

sleep 2
adb shell input tap 1000 270
sleep 2

adb shell input tap 700 2400
sleep 2


adb -e uninstall com.example.dvs_driver_mirror
