#!/bin/bash

# Local directories
DOWNLOADS="$HOME/Downloads"
BASHRC="$HOME/.bashrc"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'



ANDROID_STUDIO_URL="https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2023.3.1.18/android-studio-2023.3.1.18-linux.tar.gz"
ANDROID_TOOLS_URL = "ttps://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip -O commandlinetools.zip"

sudo apt update

if java -version &>/dev/null; then
    echo "${GREEN}Java was installed${NC}"
  else
    echo "${GREEN}Installing java${NC}"
    sudo apt install -y default-jdk
fi


if [ ! -f $DOWNLOADS/android-studio* ] && [[  ! -d ${HOME}/android-studio* ]]; then
    (cd $DOWNLOADS; wget $ANDROID_STUDIO_URL;wget $ANDROID_TOOLS_URL)
    if [ ! -f $DOWNLOADS/android-studio* ]; then
        echo -e "${RED}zip not found. Download failed?${NC}"
        exit
    else
        echo -e "${GREEN}Downloaded $STUDIO_ZIP${NC}"
    fi
fi

STUDIO_ZIP=` ls $DOWNLOADS | grep "android-studio" `

if [ ! -d $HOME/android-studio ]; then
    tar -xvzf $DOWNLOADS/$STUDIO_ZIP -C $HOME 
    if [ ! -d $HOME/android-studio* ]; then
        echo -e "${RED}File not found. Extract failed ?${NC}"
        exit
    fi
fi

STUDIO_DIR=` ls $HOME | grep "android-studio" `

echo -e "${GREEN} Android studio installed !${NC}"
echo -e "${GREEN} Creating virtial device !${NC}"

# Android command line tools instalation
sudo apt install sdkmanager
sudo apt install google-android-emulator-installer

mkdir -p $HOME/Android/Sdk/cmdline-tools
unzip commandlinetools.zip -d $HOME/Android/Sdk/cmdline-tools
mv $HOME/Android/Sdk/cmdline-tools/cmdline-tools $HOME/Android/Sdk/cmdline-tools/latest

export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
export PATH=$ANDROID_HOME/platform-tools:$PATH

source $HOME/.bashrc

# Android virtual device setup
chmod +x AvdSetup.sh



cd $HOME; ./$STUDIO_DIR/bin/studio.sh