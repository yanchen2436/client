#! /bin/bash

sudo mount -t nfs 192.168.10.200:/home/admin/share /mnt/img
cd /home/nano/client
python3 close.py
python3 client_log.py

