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

3. For MacOS users: Tick the following options when installing
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




