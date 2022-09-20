# Length Calculator
An industry specific calculator to calculate the total length of a metal tally list.
This app is designed to run on a Raspberry Pi 3b with a [10.1" 1920x1200 touch screen](https://www.amazon.com/gp/product/B095R6SXX1/ref=ox_sc_act_title_2?smid=AA3SELAX5GFYF&th=1).

## Install steps

1. Install packages ```sudo apt install anjuta python3-rope libgtk-3-dev xautomation```
2. Copy contents of src directory to a folder on the pi.
3. Make the python script executable ```sudo chmod +x length_calc.py```
4. Change line 28 in length_calc.py to be the full path to the length_calc.ui file.
5. Set the app to auto start on boot. Add a file ```~.config/autostart/calc.desktop``` containing the following
```
[Desktop Entry]
Type=Application
Name=Length calculator
Exec=/home/pi/length_calculator/length_calc.py
```

## NumLock on at boot

1. Install package ```sudo apt-get install numlockx```
2. Add file ```~.config/numlock.sh``` containing the following
```bash
#! /bin/bash

numlockx on
```
3. Make the file executable ```sudo chmod +x numlock.sh```

## Add company logo startup png

[Directions here](https://www.tomshardware.com/how-to/custom-raspberry-pi-splash-screen)

## Switching to dark theme.
[Taken from here](https://chargedwarrior.com/how-to-customize-raspberry-pi-display-theme-splash-screen/)

1. Run the following command ```sudo apt remove lxappearance-obconf```
2. Main Menu > Preference > Theme and Appearance Settings
3. Change theme to Adwaita-dark, and change font to 24 pt.


# Here is what it should look like.

![image](https://user-images.githubusercontent.com/24275193/191248368-a2597832-c9b7-409f-bef3-a1491084b53c.png)


