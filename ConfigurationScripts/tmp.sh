#!/bin/bash

RED='\033[1;31m'
BLUE='\033[1;36m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

echo -e "${RED} Log.txt created for logging !${NC}"


DOWNLOADS=$HOME/Downloads
BASHRC=$HOME/.bashrc

STUDIO_URL="https://dl.google.com/dl/android/studio/ide-zips/3.3.0.20/android-studio-ide-182.5199772-linux.zip"



#install JAVA

echo -e "${BLUE}Adding JDK to PPA repository${NC}"

sudo add-apt-repository ppa:webupd8team/java -y >> log.txt 2>&1 && echo -e "${GREEN} Success !${NC}" ||  (echo -e "${RED} Failed !${NC}" ; exit)
echo -e "${BLUE}Installing JDK 8${NC}"
sudo apt-get install oracle-java8-installer -y

echo -e "${BLUE}Setting JDK 8 as default${NC}"
sudo apt-get install oracle-java8-set-default  -y  && echo -e "${GREEN} Success !${NC}" ||  (echo -e "${RED} Failed !${NC}" ; exit)


# download android studio if needed

if [ ! -f $DOWNLOADS/android-studio* ] && [[  ! -d ${HOME}/android-studio* ]]; then
    (cd $DOWNLOADS; wget $STUDIO_URL)
    #verify download finished
    if [ ! -f $DOWNLOADS/android-studio* ]; then
        echo -e "${RED}zip not found. Download failed?${NC}"
        exit
    fi
fi
STUDIO_ZIP=` ls $DOWNLOADS | grep "android-studio" `


# Extract android studio to home

echo -e "${BLUE}\nExtracting android studio to $HOME${NC}"

if [ ! -d $HOME/android-studio ]; then
    unzip $DOWNLOADS/$STUDIO_ZIP -d $HOME  >> log.txt 2>&1 && echo -e "${GREEN} Success !${NC}" ||  (echo -e "${RED} Failed !${NC}" ; exit)
    if [ ! -d $HOME/android-studio* ]; then
        echo -e "${RED}File not found. Extract failed ?${NC}"
        exit
    fi
fi

echo -e "${GREEN} Success !${NC}"


# Run android studio for installation

STUDIO_DIR=` ls $HOME | grep "android-studio" `

echo -e "${BLUE}\nExecuting setup for android studio (Close Android studio when installation is completed) ${NC}"

(cd $HOME; ./$STUDIO_DIR/bin/studio.sh >> log.txt 2>&1 && echo -e "${GREEN} Success !${NC}" ||  (echo -e "${RED} Failed !${NC}" ; exit))

echo -e "${GREEN} Android studio installed !${NC}"

# Setting Android Studio environment variables

echo -e "${BLUE}Setting Android Studio environment variables ($BASHRC)${NC}"


ANDROID_HOME=$(cat $BASHRC | grep "ANDROID_HOME")

if [ -z "$ANDROID_HOME"  ]; then
    echo -e "\n# Android Studio environment variables" >> $BASHRC
    echo "export ANDROID_SDK_ROOT=$HOME/Android/Sdk" >>  $BASHRC
    echo "export ANDROID_HOME=$ANDROID_SDK_ROOT" >>  $BASHRC

    source $HOME/.bashrc

    echo "export PATH=\$PATH:$HOME/Android/Sdk/tools:$HOME/Android/Sdk/platform-tools" >>  $BASHRC
    if [ ! -z "$ANDROID_HOME"  ]; then
        echo -e "${RED}ANDROID_HOME not set. Android Environment failed ?${NC}"
        exit
    fi
fi
echo -e "${GREEN} Success !${NC}"
