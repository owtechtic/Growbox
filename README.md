# Growbox
This script is for a system that monitors water level, temperature, and humidity and controls water circulation and UV lights in a deep water hydroponic system
In addition to downloading the two scripts, be sure to type the following lines into terminal on your raspberry pi: 
sudo apt-get update
sudo pip3 install adafruit-circuitpython-mcp3xxx
sudo pip3 install adafruit-blinka
sudo pip3 install Adafruit-Python-DHT
sudo pip3 install adafruit-circuitpython-charlcd
sudo apt-get install i2c-tools
sudo apt-get install python-smbus

Be sure to enable the following:
enable SPI
enable I2C
