#! /bin/bash

sudo mount -t cifs //192.168.10.200/share ~/share/image/img -o username=admin,password=admin
cd /home/nano/client
python3 close.py
python3 client_log.py

