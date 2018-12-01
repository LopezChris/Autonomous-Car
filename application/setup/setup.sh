#!/bin/bash

##
#
# Description: Bash script sets up the autonomous car development environment
# - Installs Anaconda for Python 3
#
##

##
#
# 0. Import and Initialize bash logger library
#
##

#git clone https://github.com/jmorenoamor/ksh-logger
# modified above repo for bash

LIB_PATH="../lib"
LIB_PACKAGE="bash-logger"
LIB_FILE="logger.sh"

# Load or import the logger library
. $LIB_PATH/$LIB_PACKAGE/$LIB_FILE

# Set needed configuration for values
LOG_LEVEL=4

# Path where LOG_FILE will be generated
LOG_PATH="/var/log/autonomous-car/app/setup/"
LOG_FILE="setup.log"

# Get current user
GROUP_NAME="syslog"
# Add user to syslog group to have write access to /var/log
echo "Enter sudo password: ";
read -s PW
# Change ownership of log folder to current active user
echo $PW | sudo -S chown $USERNAME:$GROUP_NAME /var/log

# Init the logger
logger_init

##
#
# 1. Download and Install Anaconda for Python 3
#
##

# Reference: https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart

# 1.1: Retrieve latest version of anaconda 
# https://www.anaconda.com/download

# 1.2: Download Anaconda Bash Script
ANACONDA_VER_SH="Anaconda3-5.2.0-Linux-x86_64.sh"
wget https://repo.anaconda.com/archive/$ANACONDA_VER_SH -O /tmp/$ANACONDA_VER_SH

# 1.3: Verify Data Integrity of Installer
PATH_TO_ANACONDA_SH="/tmp/$ANACONDA_VER_SH"
ACTUAL_CRYPTO=$(sha256sum $PATH_TO_ANACONDA_SH | grep -o "^[^ ]*")
EXPECTED_CRYPTO="09f53738b0cd3bb96f5b1bac488e5528df9906be2480fe61df40e0e0d19e3d48"
# If data integrity compromised, then log error and exit shell script
if [ "$ACTUAL_CRYPTO" != "$EXPECTED_CRYPTO" ]
then
    # Severity of Log Message written is ERROR
    LOG_LEVEL=4
    # Pass ERROR message to setup.log
    log_error "$ANACONDA_VER_SH cryptographic hash data integrity compromised, exiting"
    exit 1
fi

# 1.4: Run Anaconda Script
# You'll receive output to review license agreement, press ENTER until you reach end
bash $PATH_TO_ANACONDA_SH

# 1.5: Complete Installation Process
# Once you agree to license, in output, you'll be prompted to choose install location
# You can press ENTER to accept default location or specify location

# 1.6: Select Options
# Once the installation completes in output, 
# you'll be prompted to choose if you want the installer to prepend the Anaconda3 
# install location to PATH $HOME/anaconda3
# It's recommended you type "yes" to use "conda" command

# you'll next be prompted for PATH to store $HOME/.bashrc
# It's recommended you type "yes" to use "conda" command

# In output, you'll next be prompted if you want to install Visual Studio Code
# Type "yes" to install, else "no" to decline

# 1.7: Activate Installation
source ~/.bashrc

# 1.8: Test Installation
conda list

# 1.9: Set Up Anaconda Environments
conda create --name autonomous-car python=3

# Activate new environment
source activate autonomous-car

