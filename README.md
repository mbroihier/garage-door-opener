# Garage Door Opener 


This repository contains python programs that receive Bluetooth commands to open and close a garage door.  It does this by setting up a RFCOMM server that waits for a byte stream from a client.  The byte stream is a pseudo random stream of bytes.  The server analyzes these bytes and determines if they are from a valid client.  If they are, the server, running on a Raspberry PI 0 W single board computer, pulses a GPIO pin to close and reopen a relay.  The relay is connected to the same contacts used by a push button that is mounted near the house entry. 

Parts:
  - Raspberry PI 0 W
  - Velleman IO VMA406 5v relay
  - 16 G SD card - can be smaller
  - 110 to USB power suppy and adapter/cables to attach to the PI
  - Zebra Zero Black Ice GPIO case made by C4LABS 

Assembly - Software:
  1)  Install Stretch Lite from www.raspberrypi.org/downloads/raspbian
      I do headless installs of my PI 0's which, on the publication date
      means that I copy the raspbian image to the SD card plugged into my
      Mac, mount the card and touch the ssh file on the boot partition and
      and create a wpa_supplicant.conf file.
  2)  Boot off the installed image.
  3)  Change the password.
  4)  Change the node name to gdo.
  5)  sudo apt-get update
  6)  sudo apt-get install python-bluetooth
  7)  sudo apt-get install python3-pip
  8)  sudo pip3 install PyBluez
  9)  sudo pip3 install RPi.GPIO
 10)  edit the /etc/systemd/system/bluetooth.target.wants/bluetooth.service file
      to add --noplugin=sap -C to the ExecStart line
 11)  restart the service (sudo systemclt restart bluetooth.service) - it may
      give you some other instructions and you may need to enable it first
 12)  sudo spdtool add SP
 13)  sudo apt-get install git
 14)  git clone https://github.com/mbroihier/garage-door-opener.git
 15)  sudo cp -p GDO.service /lib/systemd/system/ 
 16)  sudo systemctl enable GDO
 17)  Pair your bluetooth client with this server
      - sudo bluetoothctl (you'll need to start the agent, allow discovery, then initiate a pairing operation from the client, disable the agent, and disable discovery)


Once paired, reboot:
```
sudo shutdown -r now

```
This will start the server.  A client like the one in https://github.com/mbroihier/GDO will be able to send messages to the server which will cause it to pulse pin 11 of the 40 pin connector. 

