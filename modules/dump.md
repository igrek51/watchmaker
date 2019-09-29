# Dump wine module
store symbolic links as the link instead of the referenced file
```bash
cd /media/igrek/watchmodules
zip -y -r /mnt/data/ext/watchmaker/modules/wine.zip wine/
```

# Any module
```bash
MODULE_NAME=android-sdk
cd /media/igrek/watchmodules
zip -y -r /mnt/data/ext/watchmaker/modules/$MODULE_NAME.zip $MODULE_NAME/
```
