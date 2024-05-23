#!/bin/bash

# Ścieżka do pliku .json
JSON_FILE="../data/data.json"

# Odczytywanie danych z pliku .json
USERNAME=$(jq -r '.username' $JSON_FILE)
PASSWORD=$(jq -r '.password' $JSON_FILE)
STATUS=$(jq -r '.status' $JSON_FILE)
DATETIME=$(jq -r '.datetime' $JSON_FILE)

# Funkcja do wysyłania tekstu za pomocą adb shell input text
send_text() {
    local text="$1"
    adb shell input text "$(printf '%s' "$text" | sed 's/ /%s/g')"
}

# Wykonywanie poleceń adb z użyciem odczytanych danych
adb -e install ../apk_files/app-debug.apk
adb shell monkey -p com.example.loginttester2 1

adb shell input tap 600 700
send_text "$USERNAME"

adb shell input tap 600 935
send_text "$PASSWORD"

adb shell input tap 600 1170
send_text "$STATUS"

adb shell input tap 600 1400
send_text "$DATETIME"

adb shell input keyevent 4

adb shell input tap 100 1450
sleep 2
adb shell input tap 600 1650

sleep 5
adb -e uninstall com.example.loginttester2
