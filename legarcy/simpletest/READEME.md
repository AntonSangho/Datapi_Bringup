# [하드웨어 검증 코드](/src/simpletest/) 
- [Blink.py](/src/simpletest/Blink.py)
- [Button.py](/src/simpletest/Button.py)
- [Buzzer.py](/src/simpletest/Buzzer.py)
- [i2C.py](/src/simpletest/i2c.py)
- [Light.py](/src/simpletest/Light.py)
- [Neopixel.py](/src/simpletest/Neopixel.py)
- [RTC.py](/src/simpletest/RTC.py)
- [sd_test.py](/src/simpletest/sd_test.py)
- [Temp.py](/src/simpletest/Temp.py)

# sdcard fortmat 명령어 
sudo umount /dev/sdc1	# Unmount the SD card
sudo parted /dev/sdc --script -- mklabel msdos	# Create a new partition table
sudo parted /dev/sdc --script -- mkpart primary fat32 1MiB 100%	# Create a new partition
sudo mkfs.vfat -n SDCARDC -F32 /dev/sdc1	# Format the partition
sudo parted /dev/sdc --script -- print	# Print the partition table
