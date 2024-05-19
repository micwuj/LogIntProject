#!/bin/bash

# Create a configuration file for the AVD
CONFIG_FILE="device_config.ini"

# Create the AVD
avdmanager --verbose create avd --force --name "executoner" --package "system-images;android-34;google_apis_playstore;x86_64" --tag "google_apis_playstore"


# Start the emulator
emulator -avd Pixel_executoner
