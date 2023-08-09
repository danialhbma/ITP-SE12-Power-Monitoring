# M5StickC
- [Devices Used](#devices-used)
- [M5StickC Setup](#m5stickc-setup)
    - [Install FTDI Driver](#install-ftdi-driver)
    - [Firmware Burning](#firmware-burning)
- [Visual Studio Code Setup](#visual-studio-code-setup)
   - [Install VSCode and M5Stack Extension](#install-vscode-and-m5stack-extension)
   - [Set M5StickC to USB Mode](#set-m5stickc-to-usb-mode)
   - [Test M5StickC Setup](#test-m5stickc-setup)
- [Project Codes](#project-codes)
- [Running Project Codes in M5StickC](#running-project-codes-in-m5stickc)
   - [Load Codes into M5StickC](#load-codes-into-m5stickc)
   - [Run in App Mode](#run-in-app-mode)
     
## Devices Used
| Device Used | Link | 
| --- | --- |
| M5Stick C | https://shop.m5stack.com/products/stick-c |
| Temperature Sensor | https://shop.m5stack.com/products/m5stickc-env-hat-sht30-bmp280-bmm150 |
| CO2 Sensor | https://shop.m5stack.com/products/tvoc-eco2-gas-unit-sgp30 |
| Light Sensor | https://shop.m5stack.com/products/light-sensor-unit |
| Water Flow Sensor | https://wiki.dfrobot.com/Water_Flow_Sensor_-_1_2__SKU__SEN0217 |
| USB Type-C Cable | - |

## M5StickC Setup
This is the initial setup required when using new M5StickC devices. The guide is based on the official M5Stack tutorial: https://docs.m5stack.com/en/quick_start/m5stickc/mpy

### Install FTDI Driver
The FTDI USB Serial Port driver helps operating systems communicate with USB Serial Port devices, which will be needed
1. Install the FTDI driver based on operating system: https://ftdichip.com/drivers/vcp-drivers/
2. For Windows users: Install the driver file directly in Device Manager. Installing by running the executable driver file might not work properly.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/f1d0ae8a-89ae-48b3-9eea-0da3107de058)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c17c9de3-a139-4480-8270-3ae2acb4e6b9)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/b6a48aae-cdaf-411f-b243-7c054c3d71d5)


4. For MacOS users: Tick the following options when installing
System Preferences > Security and Privacy > General > Allow downloadable apps from the following locations > App Store and Approved Developer Options
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/b0e49520-0800-4a38-a79d-cc2246cc3dd9)


### Firmware Burning
1. Download the M5Burner firmware burning tool according to your operating system:

| Operating System | Link to Burner Software | 
| --- | --- |
| Windows | https://m5burner.m5stack.com/app/M5Burner-v3-beta-win-x64.zip |
| MacOS | https://m5burner.m5stack.com/app/M5Burner-v3-beta-mac-x64.zip |
| Linux | https://m5burner.m5stack.com/app/M5Burner-v3-beta-linux-x64.zip |

2. After downloading, unzip the file and open the M5Burner application.
    1. For Windows users:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/6ab08b56-c28c-4ea3-9ef8-c95ff06f5b7e)

    2. For MacOS users: Move the M5Burner application into Applications folder as shown:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/fd207c87-e17a-4c50-8173-e7e7c8c70214)


    3. For Linux users: cd into the decompressed file path and run 
    ```
    ./M5Burner
    ```

3. Select StickC from the list > Select the version (v1.11.9 was used) > Click Download
![Downloading Firmware](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/a7e54d19-764a-420a-be5e-a868fe98b075)

4. Connect the M5StickC to the computer using a USB Type-C Cable
5. Configure Wifi settings
![Config](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/350c1e6d-5ed3-42d8-8e9f-04bd5a81be1d)

6. Click Burn. The burner application will automatically select the COM port and set the default baud rate.
![Burn](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/8b07fc40-7f11-427b-ba66-33d3e7a99ff1)

7. Firmware burned successfully
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/7a02a941-756b-4000-8fd4-ad178d326f87)



## Visual Studio Code Setup
### Install VSCode and M5Stack Extension
The m5stack extension is required to code using Visual Studio Code IDE

1. Install Visual Studio Code IDE from https://code.visualstudio.com/
2. Launch Visual Studio Code
3. Navigate to Extensions > Search "m5stack" > Click Install
![install vscode ext](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/0a451b0d-dd54-4f7f-87c7-9cca2b4276a9)

### Set M5StickC to USB Mode
1. Connect the M5StickC to computer via a USB Type-C Cable
2. Press and hold the power button on the left side of the device to power on/restart
3. When the M5StickC powers up, quickly press the right button to switch to USB mode
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/381a39ec-c334-44f0-b6b5-28062e1dc9eb)


### Connect to M5StickC in VSCode
1. In the bottom left corner of VSCode IDE, click Add M5Stack

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2cd1f5ff-51d0-4caf-a271-2f13197842ce)

2. Select the corresponding device port
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/184168d2-c008-4fe4-9d83-04e12ecf6062)


3. If the device is successfully added, you should be able to view the device files in the left menu under M5Stack Device:

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/72342775-807b-4651-bd03-7338f3da9339)

### Test M5StickC Setup
1. To test the installation and setup, replace main.py with the following code:
```
from m5stack import *
from m5ui import *
from uiflow import *

M5Led.on()
```

2. Click the Run button > Select Run in M5Stack
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/9492a8c8-a184-4fa2-91b0-15cff84c164b)

3. If the M5StickC LED lights up as shown, installation and setup is successful
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/9956a1ad-e4c8-4209-a02d-5aea3bf2d50c)

## Project Codes
This section briefly describes each code file in this repository

| Code File | Description | 
| --- | --- |
| main.py | Allow user to select a sensor and a rack, connects to Wi-Fi and MQTT, reads sensor data, publishes it, and then goes into deep sleep until the next cycle |
| sensorinterface.py | Standardise all sensor operations and force read/publish | 
| publisher.py | Handles connection to MQTT broker and publishing | 
| wifi.py | Handles connection to wifi | 
| light.py | Retrieves data from light sensor and sends data via MQTT | 
| tvoctemp.py | Retrieves data from temperature and CO2 sensors and sends data via MQTT | 
| waterflow.py | Retrieves data from water sensor and sends data via MQTT | 
| clamp.py | Retrieves data from AC current sensor and sends data via MQTT | 
| ambient.py | Retrieves data from ambient light sensor and sends data via MQTT | 
| dfrobot_b_lux_v30b.py | Arduino library for ambient light sensor converted into MicroPython | 

## Running Project Codes in M5StickC
### Load Codes into M5StickC
1. Connect the M5StickC to computer via a USB Type-C Cable
2. [Set M5StickC to USB Mode if you haven't done so](#set-m5stickc-to-usb-mode)
3. After adding M5StickC in VSCode, copy and paste the main.py codes into the device's main.py file. **Note: using the upload button for main.py might not work in overwriting the original main.py file** 
4. Press the Upload button > Upload all Python code files (except main.py) from this repository into the main folder:
![upload](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/aaaa5977-b6d2-48fb-a242-6ce06139c1a0)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/89905b4d-7fd4-4303-aa75-f6d8b6ba5e6b)


   
5. The files should look like this:

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/153e2007-970a-4432-b0bc-fc0a1e533da9)

   
### Run in App Mode
The M5Stick should be switched to App Mode prior to deployment and configured based on the sensors connected.
**Important: The sensor and rack settings will be lost if the M5Stick loses power/is rebooted. The selection of sensors and racks must be completed upon reboot**

1. Connect all desired sensors 
2. Press and hold the power button on the left side of the device to power on/restart
3. When the M5StickC powers up, quickly press the right button to switch to App mode
4. Use the right button to scroll down and the middle button to select the corresponding option on the UI based on the sensors connected:

| Option | Sensors Connected | 
| --- | --- |
| Water | Water Flow Sensor | 
| TVOC/Temp | CO2 and Temperature Sensor | 
| Light | Light Sensor | 

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/32ba171d-2692-4394-b3de-43011f2ea8af)


5. Select the coresponding rack from the menu

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/7eec669d-0d2e-4150-b6ec-b091ef43caed)

6. The M5Stick is now deployed successfully

