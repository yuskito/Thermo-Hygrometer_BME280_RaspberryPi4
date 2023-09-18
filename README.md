
# Welcome to Thermo-Hygrometer-BME280-RaspberryPi4

## About this project
I made a Thermo-Hygrometer with BME280 and Raspberry Pi4.

## How it looks like 
On the Raspberry Pi display, a window will show up like this and displays temperature (in Celsius and Fahrenheit), humidity and pressure.<br>

![](../Thermo-Hygrometer-BME280-RaspberryPi4/.README_images/GUI_image.png)

## How it works
- Raspberry Pi reads out sensor values from BME280 via I2C communication and Raspberry Pi display the information on a window on HDMI display.<br>

![](../Thermo-Hygrometer-BME280-RaspberryPi4/.README_images/Diagram.png)
- 
- Raspberry runs a code in Python. 
- Tkinter is used for GUI part of code.

## Hardware needed
1. Raspberry Pi4 <br>
   (I used Raspberry Pi 4B)<br>


2. BME280 module <br> 
- BME280 is a sensor IC from Bosch. 
It measures temperature, humidity and pressure.
It has a very good accuracy.
- I used BME280 module kit from Akiduki though, I think any modules with BME280 chio would work. <br>
   https://akizukidenshi.com/catalog/g/gK-09421/

![](../Thermo-Hygrometer-BME280-RaspberryPi4/.README_images/BME280_image.png)

3. Some jumper wires and solders

## How to connect BME280 and Raspberry Pi4 
Connect pins as below.

| BME280 | Raspberry Pi 4 | 
|------|----------------|
| VDD  | 3.3v (Pin1)    |
| GND  | GND (Pin9 or Pin 14)|
| CSB  | Not connected  |
| SDI  | GPIO2 (Pin3)   |
| SDO  | GND (Pin9 or Pin 14)|
| SCK  | GPIO3 (Pin5)   |

Note: This is for BME280 module from Akiduki. <br> 
For other devices, please follow the instruction of the module you use.<br>
If you use BME280 module from Akiduki, make sure that you solder on J3 to activate I2C instead of SPI as in the instruction of the module.

## How to set up environment on Raspberry Pi4

1. OS: I used  Raspberry Pi OS ( Kernel version: 6.1, Debian version: 11 (bullseye)).
<br>Anything else should work, but please make sure you use Python3. <br><br>

2. Python version:  This code works in Python 3, but does not work on Python2.<br><br>

3. Python modules:
- smbus2: To use I2C communication. You need to install smbus2 library. Run the following command on terminal. <br>
`$ sudo pip install smbus2` <br><br>

- Tkinter: This code uses Tkinter library for GUI part.<br>
    you need to install Tkinter to run this code.<br>
Run the following command on terminal to install Tkinter <br>
`$ sudo apt-get install python3-tk`<br><br>

- Schedule: This code uses Schedule library to run some codes periodically - 
get the sensor values from BME280 and refresh the screen periodically.     
`$ pip install schedule`<br><br>
Note: The command above may be different depending on your environment (OS and python and pip version etc.)
## How to run the code
1. Download zip file and extract, or clone in Github.
2. Open the terminal and go to "Thermo-Hygrometer-BME280-RaspberryPi4" directory using cd command.
3. Run the following command in terminal.<br>

`$ python main.py`
4. Then, a window should pop up and displays the values from BME280 sensor.<br><br>

5. Optional: For debugging purpose, I made an option to run this program with offline debugging mode - without BME280 module connected. <br>
If you run the following command in the terminal,<br>

`$ python main.py --OD`<br>
- A window pops up, but the values are not from BME280, but pre-set constant values.<br>
This mode is useful to identify the issue (hardware issue vs. software issue) and to develop the code with another computers without BME280<br><br>

## 3dr party license
This code uses "BME280" library from Switch Science with some modifications. <br>
Copyright (c) 2018 Switch Science<br>
Please see the following link for details of this library.
https://github.com/SWITCHSCIENCE/BME280.git
