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

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2d5306f7-a931-42d2-817f-9fec8e78ed74)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/597c1d81-8fc9-4b77-a101-1b655d681aeb)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c69396c3-428a-4b4e-92b1-0da780bf9d5b)

4. For MacOS users: Tick the following options when installing
System Preferences > Security and Privacy > General > Allow downloadable apps from the following locations > App Store and Approved Developer Options
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/e291130b-5801-4876-a256-21de9c2674c4)

### Firmware Burning
1. Download the M5Burner firmware burning tool according to your operating system:

| Operating System | Link to Burner Software | 
| --- | --- |
| Windows | https://m5burner.m5stack.com/app/M5Burner-v3-beta-win-x64.zip |
| MacOS | https://m5burner.m5stack.com/app/M5Burner-v3-beta-mac-x64.zip |
| Linux | https://m5burner.m5stack.com/app/M5Burner-v3-beta-linux-x64.zip |

2. After downloading, unzip the file and open the M5Burner application.
    1. For Windows users:
  ![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/8b27dee7-3f68-4bcf-9b85-61cfe5f211cc)
    
    2. For MacOS users: Move the M5Burner application into Applications folder as shown:
  ![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c8a7ce39-9e7e-4e77-aee7-5ab835938498)
    
    3. For Linux users: cd into the decompressed file path and run 
    ```
    ./M5Burner
    ```

3. Select StickC from the list > Select the version (v1.11.9 was used) > Click Download
![Downloading Firmware](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/12ced48d-e18a-4eeb-a697-689540347181)

4. Connect the M5StickC to the computer using a USB Type-C Cable
5. Click Burn
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/1274f9de-980a-4a67-9f3c-8cd9d48a13b7)

6. Configure Wifi settings
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2d7a18b8-3603-45b6-881f-02ae7f450a0c)

7. Click Burn. The burner application will automatically select the COM port and set the default baud rate.
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/1b59332d-a4a2-4d40-b84c-6922549df465)

8. Firmware burned successfully
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/ed6d2e9d-664a-4b27-9a61-766ef5d70306)


## Visual Studio Code Setup
### Install VSCode and M5Stack Extension
The m5stack extension is required to code using Visual Studio Code IDE

1. Install Visual Studio Code IDE from https://code.visualstudio.com/
2. Launch Visual Studio Code
3. Navigate to Extensions > Search "m5stack" > Click Install
![install vscode ext](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c091d58b-ae97-487d-9f9b-3da15ef5ff0e)

### Set M5StickC to USB Mode
1. Connect the M5StickC to computer via a USB Type-C Cable
2. Press and hold the power button on the left side of the device to power on/restart
3. When the M5StickC powers up, quickly press the right button to switch to USB mode
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/5bd2a63e-83b5-4772-9ccf-bbb4785188b2)

### Connect to M5StickC in VSCode
1. In the bottom left corner of VSCode IDE, click Add M5Stack
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2540b724-6208-4e34-a623-b3d8bbb96c5f)

2. Select the corresponding device port
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/027f6a9f-51ac-412b-90e8-7905a9910b81)


3. If the device is successfully added, you should be able to view the device files in the left menu under M5Stack Device:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2bcab7df-44de-40d7-a1d5-401947183725)

### Test M5StickC Setup
1. To test the installation and setup, replace main.py with the following code:
```
from m5stack import *
from m5ui import *
from uiflow import *

M5Led.on()
```

2. Click the Run button > Select Run in M5Stack
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/d2418ea7-da3a-4880-b790-647ab89d20a8)

3. If the M5StickC LED lights up as shown, installation and setup is successful
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/5509931c-d4fd-4149-8b00-7e6ff82f8974)

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
![upload](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/07e41918-81f6-400c-b6da-35ebf0399042)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/666cd8dc-ff00-44d5-ab9c-ba7fa56e5dbd)

   
5. The files should look like this:

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/3f9b2142-197c-464a-a251-e2f684f92611)

   
### Run in App Mode
The M5Stick should be switched to App Mode prior to deployment and configured based on the sensors connected.
1. Connect all desired sensors 
2. Press and hold the power button on the left side of the device to power on/restart
3. When the M5StickC powers up, quickly press the right button to switch to App mode
4. Use the right button to scroll down and the middle button to select the corresponding option on the UI based on the sensors connected:

| Option | Sensors Connected | 
| --- | --- |
| Water | Water Flow Sensor | 
| TVOC/Temp | CO2 and Temperature Sensor | 
| Light | Light Sensor | 

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/ff5dab08-151f-4a19-8c86-097adc46e9bc)

5. Select the coresponding rack

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/7de86174-70ca-4fb6-affe-2453c347d803)

6. The M5Stick is now deployed successfully

