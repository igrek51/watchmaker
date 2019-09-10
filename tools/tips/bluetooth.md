install pulseaudio-alsa pulseaudio-bluetooth bluez bluez-libs bluez-utils bluez-utils-compat rfkill pulseaudio-module-bluetooth

# generic bluetooth driver
modprobe btusb

sudo systemctl start bluetooth
rfkill block bluetooth
rfkill unblock bluetooth

rfkill list
rfkill unblock 6

# bluetoothctl
Possibly select a default controller by inputting:
# select <MAC Address>
# power on
# agent on
# default-agent
# scan on
# devices
# remove 00:11:67:2C:EE:8D
# pair 00:11:67:2C:EE:8D
If using a device without a PIN, one may need to manually trust the device before it can reconnect successfully. Enter: # trust <MAC Address> to do so.
# connect 00:11:67:2C:EE:8D
# scan off
# exit

If not connecting:
# sudo apt install pulseaudio-module-bluetooth 
# pulseaudio -k
# pulseaudio --start
If restarting PulseAudio does not work, you need to load module-bluetooth-discover:
# sudo pactl load-module module-bluetooth-discover
If that still does not work, also load the following PulseAudio modules:
module-bluetooth-policy
module-bluez5-device
module-bluez5-discover
Or try to run "scan off" earlier

pavucontrol
	Configuration:
		Philips SHB5850: Profile: Sink A2DP
	Output Devices:
		Philips SHB5850:
			set as fallback
			set volume
	Playback:
		application:
			set output: Philips SHB5850
