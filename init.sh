#! /bin/bash

# 设置远程服务器的IP地址，可以替换成你自己的服务器
remote_server="192.168.10.200"

# 设置最大尝试次数
max_attempts=10
current_attempt=1

# 循环直到 ping 成功或达到最大尝试次数
while [ $current_attempt -le $max_attempts ]; do
  # 尝试ping远程服务器一次
  ping -c 1 $remote_server > /dev/null 2>&1

  # 检查ping命令的退出状态
  if [ $? -eq 0 ]; then
    echo "网络已启动，可以连接到远程服务器。"

    # 在这里可以继续执行你的其他操作
    sudo mount -t nfs 192.168.10.200:/home/admin/share /mnt/img

    cd /home/nano/client
    python3 close.py
    python3 client_log.py

    break  # 跳出循环，因为成功了

  else
    echo "第 $current_attempt 次尝试失败，等待3秒后重试..."
    sleep 3
    ((current_attempt++))
  fi
done

if [ $current_attempt -gt $max_attempts ]; then
  echo "尝试达到最大次数，无法连接到远程服务器。"
fi
