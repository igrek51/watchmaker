#!/bin/bash
echo "Turning on bluetooth modules.."
sudo modprobe btusb
sudo systemctl start bluetooth

# resetting bluetooth
echo "Resetting bluetooth via rfkill..."
sudo rfkill block bluetooth
sudo rfkill unblock bluetooth

echo "Verify bluetooth is enabled"
sudo rfkill list
# sudo rfkill unblock 6

export LOCAL_DEVICE_MAC="28:C6:3F:09:81:10"
export REMOTE_DEVICE_MAC="00:11:67:2C:EE:8D"

echo "Connecting to device"
bluetoothctl << EOF
select $LOCAL_DEVICE_MAC
power on
agent on
default-agent
scan on
devices
remove $REMOTE_DEVICE_MAC
pair $REMOTE_DEVICE_MAC
connect $REMOTE_DEVICE_MAC
scan off
exit
EOF

sleep 3
bluetoothctl << EOF
connect $REMOTE_DEVICE_MAC
exit
EOF

echo "check in pavucontrol..."
cat << EOF
Configuration:
	Philips SHB5850: Profile: Sink A2DP
Output Devices:
	Philips SHB5850:
		set as fallback
		set volume
Playback:
	application:
		set output: Philips SHB5850
EOF

pavucontrol &

echo "Testing audio..."
lich test audio

audacious "/home/user/Music/Stairway to Heaven.mp3"
