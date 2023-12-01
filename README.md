# client
该项目为一个socket客户端，主要的功能是在jetson nano上控制工业相机拍照。
# init.sh
该文件为开机自启动脚本，用于挂载nfs共享文件夹，方便写入文件至服务器。但jetson nano开机时可能会出现网络服务还没启动就先运行该脚本，导致挂载失败。所以在运行开始前先ping通再进行挂载。
# client_nfs.py||cilent_read.py
python文件是主要运行程序，解析jetson，失败指令，设置参数，调用拍照脚本。
# open.py||close.py
这两个就是激光的开关脚本。
# csave.py
拍照脚本，拍照后存入共享文件夹。
# width.py
用于标记照片截取范围。
