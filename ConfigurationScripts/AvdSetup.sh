#!/bin/bash

# Create a configuration file for the AVD
CONFIG_FILE="device_config.ini"
AVD_LOCATION="$HOME/.android/avd/executoner.avd"
RAM_SIZE=6144

# Create the AVD
# avdmanager --verbose create avd --force --name "executoner" --package "system-images;android-34;google_apis_playstore;x86_64" --tag "google_apis_playstore"
# cp $CONFIG_FILE $AVD_LOCATION/config.ini

sed -i "s/^hw.ramSize=.*/hw.ramSize=$RAM_SIZE/" "$AVD_LOCATION/config.ini"
echo "Size of ram changed to: $RAM_SIZE"


# IDEA DROPED - włączanie ręczne
# Start the emulator
# emulator -avd executoner
