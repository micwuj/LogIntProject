#!/bin/bash

# Create a configuration file for the AVD
CONFIG_FILE="device_config.ini"
AVD_LOCATION="$HOME/.android/avd/Pixel_3a_API_34.avd"

# Create the AVD
# avdmanager --verbose create avd --force --name "executoner" --package "system-images;android-34;google_apis_playstore;x86_64" --tag "google_apis_playstore"
cp $CONFIG_FILE $AVD_LOCATION/config.ini


# Start the emulator
# emulator -avd executoner
