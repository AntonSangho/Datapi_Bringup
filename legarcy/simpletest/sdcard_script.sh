#!/bin/bash

# 스크립트를 루트 권한으로 실행해야 합니다.
if [ "$EUID" -ne 0 ]; then
  echo "이 스크립트는 루트 권한으로 실행되어야 합니다."
  exit 1
fi

# /dev/sda1 파티션을 언마운트합니다.
echo "Unmounting /dev/sda1..."
sudo umount /dev/sda1

# /dev/sda 디스크의 파티션 테이블을 msdos 형식으로 생성합니다.
echo "Creating a new msdos partition table on /dev/sda..."
sudo parted /dev/sda --script -- mklabel msdos

# /dev/sda 디스크에 1MiB에서 시작하여 전체 디스크를 사용하는 fat32 형식의 primary 파티션을 생성합니다.
echo "Creating a new primary FAT32 partition on /dev/sda..."
sudo parted /dev/sda --script -- mkpart primary fat32 1MiB 100%

# 파티션 테이블을 다시 읽도록 시스템에 알립니다.
echo "Informing the system to re-read the partition table..."
sudo partprobe /dev/sda

#잠시 대기하여 파티션이 생성되었는지 확인합니다.
sleep 5

# 생성된 /dev/sda1 파티션을 FAT32 파일 시스템으로 포맷하고 라벨을 SDCARD로 설정합니다.
echo "Formatting the partition /dev/sda1 to FAT32 and labeling it as SDCARD..."
sudo mkfs.vfat -n SDCARD -F32 /dev/sda1

# 파티션 정보를 출력합니다.
echo "Printing the partition table of /dev/sda..."
sudo parted /dev/sda --script print


# SD 카드를 안전하게 제거합니다.
echo "Ejecting the SD card..."
sudo eject /dev/sda


echo "Script execution completed."

