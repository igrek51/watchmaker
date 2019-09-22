#!/bin/bash
#
# Watchmaker live initializer script
#

echo "$(id) - $(date)" >> /mnt/watchmodules/init/init.log

# release version
# cp /mnt/watchmodules/init/version/.osversion /home/user/.osversion

# add application launchers
cp /mnt/watchmodules/init/applications/*.desktop /home/ireneusz/.local/share/applications/
