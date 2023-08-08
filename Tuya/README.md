## Guide to setup Atorch S1 Socket
1. Plug the device into a power socket and turn it on. Once device is turned on, you should see this screen (This happens if the device is new or not configured to an available WiFi network around you).

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/SocketInitialScreen.jpg)

2. From the main page, press and hold M to enter menu page
3. Then, press M repeatedly until you reach 12: Wifi Device Reset

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/SocketMenuScreen.jpg)

4. Press and hold M to reset

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/SocketWorkingScreen.jpg)

5. Once done, you can start setting up the Smart Life app.

## Smart Life App (Tuya Devices)
1. Download the Smart Life app by Volcano Technology from the app store on your device (smartphone/tablet)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/SmartLifeApp.png)

2. Once downloaded, open the app and click on sign up if you're a new user. Else, proceed to login.

3. Now, you can plug in your tuya device and turn it on. (If the device is an Atorch S1 socket, please refer to the guide to set up the socket)

4. Then, you can start adding your tuya devices by clicking on the '+' button on the top right and then, clicking on 'Add Device'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppMainScreen.jpg)

5. Make sure to turn on Bluetooth so that the app can detect the device.
6. Once detected, you can click on the 'Add' button.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppAddDeviceScreen.jpg)


7. Then, enter the Wi-Fi information accordingly and click on 'Next'. The app will initially set the Wi-Fi that your smartphone/tablet is currently on.
  - If you're unable to add the device to the app, please check that Bluetooth is on and that you're connected to 2.4 GHz Wifi network (based on the device's network compatibility).

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppWifiScreen.jpg)

8. Wait for the device to be added. Once successfully, click on the pen icon to change the name of the device.
  - Note that the device name should follow these conditions (according to the Node-RED flow for Tuya API - Refer to the Tuya API section)
    - if device is monitoring growlight - 'Light' should be in the name (eg: Rack 1 Light)
    - if device is monitoring water pump - 'Water' should be in the name (eg: Rack 1 Water)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppSuccessScreen.jpg)


9. After renaming the device, click on 'Done' and now the device is successfully added.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppFinalScreen.jpg)

10. Now, you will need to link this app to your Tuya Cloud project in the Tuya IoT Platform.

For more documention on this, refer to https://developer.tuya.com/en/docs/iot/user-manual-for-tuya-smart-v3177?id=K9obrofrfk4sk

## Tuya IoT Platform Setup
1. For new users, sign up for the Tuya IoT Platform via https://auth.tuya.com/register
2. Then, proceed to login to the platform via https://auth.tuya.com/
3. Once logged in, you will be at the main page. Now, to link your Smart Life app, you will need to create a new Tuya Cloud project. So, click on the 'Cloud' option on the left hand and click on 'Development'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaCloudPage.png)

4. Then, click on 'Create Cloud Project' and fill up the necessary details in the form before clicking on 'create' button.
    - Please make sure that for 'Data center' field, Central Europe Data Center is selected and for 'Development Method' field, Custom is selected.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaNewProject.png)

5. Next, select the required API services as shown on the Selected API Service side and click 'Authorize'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaProjectAPIs.png)

6. Then, the project is created successfully

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaProjectSuccess.png)

7. Now, link your Smart Life app to the project by clicking on 'Open Project' and then clicking on 'Devices'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaProjectSuccess.png)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaCreatedProject.png)

8. Next, click on 'Link Tuya App Account' and then, click on 'Add App Account'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaLinkApp.png)

9. A QR code should pop up. 

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaQRCode.png)

10. Scan that QR code using the Smart Life App. So, open the app and click on '+' button on the top right and then, click on 'Scan'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/AppMainScreen.jpg)

11. Click on 'Confirm Login'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaConfirmLogin.jpg)

12. Set the device permissions.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaPermissions.png)

13. Now, the Smart Life app and all the devices registered in the app is connected to the project.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaAppLinkedSuccess.png)

Do note that the project is a trial edition and lasts for a month. You may either ask for an extension or upgrade the project to a paid edition. The request for extension generally takes about 1 - 2 days and it can be rejected.

Refer to this for the pricing - https://developer.tuya.com/en/docs/iot/membership-service?id=K9m8k45jwvg9j 

As for the extension, you may follow these steps:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaExtension1.png)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaExtension2.png)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/TuyaExtension3.png)



## Tuya Node-RED Flow
Make sure that these node modules are installed inside the Node-RED editor. 
Node Modules: node-red-contrib-crypto-js-dynamic (https://flows.nodered.org/node/node-red-contrib-crypto-js-dynamic) & node-red-contrib-influxdb (https://flows.nodered.org/node/node-red-contrib-influxdb) 

1. Click on the '≡' button on the top right-hand corner.
2. Then, click on manage palatte.
3. If node modules are not listed under the 'Nodes' tab, go to the 'Install' tab and install these modules.
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/Tuya/Images/NodeREDPalatteManager.png)

Refer to the Tuya Node-RED Flow Documentation.pdf & Tuya Flow.json for a more detailed explanation of the flow.