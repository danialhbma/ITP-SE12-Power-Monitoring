## Guide to setup Atorch S1 Socket
1. Plug the device into a power socket and turn it on. Once device is turned on, you should be in the main page.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/18a1d07b-1a82-4a75-add1-3e0458ad6620)

2. From the main page, press and hold M to enter menu page
3. Then, press M repeatedly until you reach 12: Wifi Device Reset

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/b39c437e-b485-42d0-8043-7d5a06e54b22)

4. Press and hold M to reset

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/3cca2ff4-9f99-4ada-9ab3-727023cb3b37)

5. Once done, you can start setting up the Smart Life app.

## Smart Life App (Tuya Devices)
1. Download the Smart Life app by Volcano Technology from the app store on your device (smartphone/tablet)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/8412e656-6928-4360-a1f9-acf2113b7f0a)
2. Once downloaded, open the app and click on sign up if you're a new user. Else, proceed to login.

3. Now, you can plug in your tuya device and turn it on. (If the device is an Atorch S1 socket, please refer to the guide to set up the socket)

4. Then, you can start adding your tuya devices by clicking on the '+' button on the top right and then, clicking on 'Add Device'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/eb417e20-f2bd-4ed9-bc3d-1819eb2bf8db)

5. Make sure to turn on Bluetooth so that the app can detect the device.
6. Once detected, you can click on the 'Add' button.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/ac84f130-bdbc-435d-b8c0-8c2532ac9900)


7. Then, enter the Wi-Fi information accordingly and click on 'Next'. The app will initially set the Wi-Fi that your smartphone/tablet is currently on.
  - If you're unable to add the device to the app, please check that Bluetooth is on and that you're connected to 2.4 GHz Wifi network (based on the device's network compatibility).

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/87879d26-924a-4ac4-8542-d4ee5e5c0edb)

8. Wait for the device to be added. Once successfully, click on the pen icon to change the name of the device.
  - Note that the device name should follow these conditions (according to the Node-RED flow for Tuya API - Refer to the Tuya API section)
    - if device is monitoring growlight - 'Light' should be in the name (eg: Rack 1 Light)
    - if device is monitoring water pump - 'Water' should be in the name (eg: Rack 1 Water)

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/c32a096a-bf79-48c7-8589-174408efcc06)


9. After renaming the device, click on 'Done' and now the device is successfully added.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/b5c45d8f-ca3b-4859-bc78-5e00e1943cf9)

10. Now, you will need to link this app to your Tuya Cloud project in the Tuya IoT Platform.

For more documention on this, refer to https://developer.tuya.com/en/docs/iot/user-manual-for-tuya-smart-v3177?id=K9obrofrfk4sk

## Tuya IoT Platform Setup
1. For new users, sign up for the Tuya IoT Platform via https://auth.tuya.com/register
2. Then, proceed to login to the platform via https://auth.tuya.com/
3. Once logged in, you will be at the main page. Now, to link your Smart Life app, you will need to create a new Tuya Cloud project. So, click on the 'Cloud' option on the left hand and click on 'Development'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/3ce46678-8d6c-46b3-b598-b7b25b73ab0c)

4. Then, click on 'Create Cloud Project' and fill up the necessary details in the form before clicking on 'create' button.
    - Please make sure that for 'Data center' field, Central Europe Data Center is selected and for 'Development Method' field, Custom is selected.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/89174520-b971-4323-b805-eae0050260a9)

5. Next, select the required API services as shown on the Selected API Service side and click 'Authorize'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/964698e1-5012-474f-b1ec-fa00695e8fa0)

6. Then, the project is created successfully

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/6b544717-9057-4673-a6d8-094d37b02659)

7. Now, link your Smart Life app to the project by clicking on 'Devices'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/f1ea448d-9da1-4988-a147-335188ec0761)

8. Next, click on 'Link Tuya App Account' and then, click on 'Add App Account'

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/03f79253-1d24-425a-b740-4f29c6ed43d8)

9. A QR code should pop up. 

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/ad5784ae-3966-4649-b276-29f0bfabdc31)

10. Scan that QR code using the Smart Life App. So, open the app and click on '+' button on the top right and then, click on 'Scan'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/4b8a3e6a-9dc8-41ab-a107-ee49cc0cd591)

11. Click on 'Confirm Login'.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/d6b5b854-6be1-4532-9636-3c0dd97c7044)

12. Set the device permissions.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/8a5fb968-9539-4654-8e2c-5725ac8c18c5)

13. Now, the Smart Life app and all the devices registered in the app is connected to the project.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/f0c85bb6-aec3-4c88-bb3f-ade3c74fb38a)

Do note that the project is a trial edition and lasts for a month. You may either ask for an extension or upgrade the project to a paid edition. The request for extension generally takes about 1 - 2 days and it can be rejected.

Refer to this for the pricing - https://developer.tuya.com/en/docs/iot/membership-service?id=K9m8k45jwvg9j 

As for the extension, you may follow these steps:
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/022bdc44-fd7f-4849-b17a-3dde35db8f1e)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/d99ebebd-f85f-42dd-9299-73cec47a6d2a)
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/142c2486-6331-4b8e-a978-81c624e098f8)



## Tuya Node-RED Flow
Make sure that these node modules are installed inside the Node-RED editor. 
1. Click on the '≡' button on the top right-hand corner.
2. Then, click on manage palatte.
3. If node modules are not listed under the 'Nodes' tab, go to the 'Install' tab and install these modules.
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/d5f2c848-4cd9-43ff-b4a0-64d169936187)

Refer to the Tuya Node-RED Flow Documentation pdf in the repository (under Tuya) for a more detailed explanation of the flow.

