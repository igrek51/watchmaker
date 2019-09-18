#!/bin/bash
#
# Watchmaker live initializer script
#

echo "$(id) - $(date)" >> /mnt/usb-data/modules/init/init.log

# release version
# cp /mnt/usb-data/modules/init/version/.osversion /home/user/.osversion

# add application launchers
cp /mnt/usb-data/modules/init/applications/*.desktop /home/ireneusz/.local/share/applications/
