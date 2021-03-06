#!/bin/bash
#
# Watchmaker live initializer script
#

echo "$(id) - $(date)" >> /mnt/watchmodules/init/init.log

# release version
# cp /mnt/watchmodules/init/version/.osversion /home/user/.osversion

# add application launchers
cp /mnt/watchmodules/init/applications/*.desktop /home/user/.local/share/applications/

# remove install-debian shortcut
rm -f /home/user/Desktop/install-debian.desktop
sudo rm -f /usr/share/applications/install-debian.desktop
