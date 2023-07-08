# M5StickC
- [Materials Used](#materials-used)
- [M5StickC Setup](#m5stickc-setup)
    - [Install FTDI Driver](#install-ftdi-driver)
    - [Firmware Burning](#firmware-buning)
- [Visual Studio Code Setup](#visual-studio-code-setup)
   - [Install VSCode and M5Stack Extension](#install-vscode-and-m5stack-extension)
   - [Set M5StickC to USB Mode](#set-m5stickc-to-usb-mode)
   - [Test M5StickC Setup](#test-m5stickc-setup)
     
# Materials Used
| Device Used | Link to Purchase | 
| --- | --- |
| M5Stick C | https://shop.m5stack.com/products/stick-c |
| Temperature Sensor | https://shop.m5stack.com/products/m5stickc-env-hat-sht30-bmp280-bmm150 |
| CO2 Sensor | https://shop.m5stack.com/products/tvoc-eco2-gas-unit-sgp30 |
| Light Sensor | https://shop.m5stack.com/products/light-sensor-unit |
| Water Flow Sensor | https://wiki.dfrobot.com/Water_Flow_Sensor_-_1_2__SKU__SEN0217 |
| USB Type-C Cable | - |

# M5StickC Setup
This guide is based on the official M5Stack tutorial: https://docs.m5stack.com/en/quick_start/m5stickc/mpy

## Install FTDI Driver
The FTDI USB Serial Port driver helps operating systems communicate with USB Serial Port devices, which will be needed
1. Install the FTDI driver based on operating system: https://ftdichip.com/drivers/vcp-drivers/
2. For Windows users: Install the driver file directly in Device Manager. Installing by running the executable driver file might not work properly.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2d5306f7-a931-42d2-817f-9fec8e78ed74)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/597c1d81-8fc9-4b77-a101-1b655d681aeb)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c69396c3-428a-4b4e-92b1-0da780bf9d5b)

4. For MacOS users: Tick the following options when installing
System Preferences > Security and Privacy > General > Allow downloadable apps from the following locations > App Store and Approved Developer Options
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/e291130b-5801-4876-a256-21de9c2674c4)

## Firmware Burning
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
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/cbc45844-ed7b-460d-9b23-0cbfc8726cba)

# Visual Studio Code Setup
## Install VSCode and M5Stack Extension
The m5stack extension is required to code using Visual Studio Code IDE

1. Install Visual Studio Code IDE from https://code.visualstudio.com/
2. Launch Visual Studio Code
3. Navigate to Extensions > Search "m5stack" > Click Install
![install vscode ext](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/c091d58b-ae97-487d-9f9b-3da15ef5ff0e)

## Set M5StickC to USB Mode
1. Connect the M5StickC to computer via a USB Type-C Cable
2. Press and hold the power button on the left side of the device to power on/restart
3. When the M5StickC powers up, quickly press the right button to switch to USB mode
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/5bd2a63e-83b5-4772-9ccf-bbb4785188b2)

## Connect to M5StickC in VSCode
1. In the bottom left corner of VSCode IDE, click Add M5Stack
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2540b724-6208-4e34-a623-b3d8bbb96c5f)

2. Select the corresponding device port
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/2b606a68-24dd-46d8-882e-ffe91e8a77de)

3. If the device is successfully added, you should be able to view the device files in the left menu under M5Stack Device:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/e5c09bfc-841b-4b31-9467-5485c328e6ea)

## Test M5StickC Setup
1. To test the installation and setup, replace main.py with the following code
```
from m5stack import *
from m5ui import *
from uiflow import *

M5Led.on()

```

2. Click the Run button > Select Run in M5Stack
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/9ec1abbf-03ef-46e8-8413-72c42e23e4ce)

3. If the M5StickC LED lights up, installation and setup is successful
