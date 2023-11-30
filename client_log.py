import socket
import threading
import subprocess
import os
import time
import logging

RECONNECT_INTERVAL = 5
proc = None

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，这将记录所有级别的日志
    format='[%(asctime)s] [%(levelname)s] %(message)s',  # 日志格式
    handlers=[
        logging.FileHandler('app_log.log'),  # 将日志记录到文件中
        logging.StreamHandler()  # 在控制台上输出日志
    ]
)
# 创建一个日志记录器
logger = logging.getLogger(__name__)


def execute_command(script_path, command):
    full_command = f"{script_path} {command}"
    subprocess.run(full_command, shell=True)


def parse_and_execute(json_data, script_path):
    global proc  # 使用全局的proc变量
    target_directory = os.path.dirname(script_path)
    for item in json_data:
        camnum = item.get('camnum', '')
        expmode = item.get('expmode', '')
        imageDir = item.get('imageDir', '')
        meagain = item.get('meagain', '')
        medgain = item.get('medgain', '')
        metime = item.get('metime', '')
        msg = item.get('msg', '')
        # 切换到目标目录
        os.chdir(target_directory)
        # logger.info("开始解析和执行")
        if camnum:
            command = f"-b {camnum} -w -f camnum -p1 {camnum}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
        if expmode:
            command = f"-b {camnum} -w -f expmode -p1 {expmode}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
        if metime:
            command = f"-b {camnum} -w -f metime -p1 {metime}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
        if meagain:
            int_part, dec_part = str(meagain).split('.')
            command = f"-b {camnum} -w -f meagain -p1 {int_part} -p2 {dec_part}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
        if medgain:
            int_part, dec_part = str(medgain).split('.')
            command = f"-b {camnum} -w -f medgain -p1 {int_part} -p2 {dec_part}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
        if imageDir:
            command = f"-b {camnum} -w -f imagedir -p1 {imageDir}"
            execute_command(script_path, command)
            logger.debug(f"执行命令: {command}")
            execute_command(script_path, f"-b {camnum} -w -f paramsave")
            logger.debug("断电保存")

        if msg == "0x00":
            logger.debug("0x00")
            # subprocess.run(["python3", "/home/nano/client/open.py"])
            # logger.debug("开始拍照")
            # proc = subprocess.Popen(["python3", "/home/nano/client/csave.py"])

        elif msg == "0xff":
            # if proc is not None:
            #     proc.terminate()
            #     logger.debug("停止拍照")
            #     proc = None
            # subprocess.run(["python3", "/home/nano/client/close.py"])
            logger.debug("0xff")

        elif msg == "0x03":
            logger.debug("开启激光")
            subprocess.run(["python3", "/home/nano/client/open.py"])

        elif msg == "0x04":
            logger.debug("关闭激光")
            subprocess.run(["python3", "/home/nano/client/close.py"])

        elif msg == "0x05":
            logger.debug("前端拍照")
            subprocess.run(["python3", "/home/nano/client/cube_save.py"])

        # logger.info("解析和执行完成")


def receive_messages(client_socket):
    # proc = None
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # print("Received message from server:", message)

            message = message.strip()  # 去除首尾空格
            if message.startswith("Broadcast from"):
                message = message.split(":")[2].strip()  # 提取出消息部分
            print("Received message from server:", message)

            # 当接收到特定消息时调用解析和执行函数
            if message.startswith("["):
                import json
                json_data = json.loads(message)
                script_path = "/home/nano/nvidia_jetson_veye_bsp-master/i2c_cmd/bin/cs_mipi_i2c.sh"
                parse_and_execute(json_data, script_path)

        except Exception as e:
            print("Error while receiving message:", str(e))
            break


def main():
    server_ip = '192.168.10.200'
    server_port = 8888

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            logger.info("已连接到服务器。")

            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()

            receive_thread.join()  # Wait for receive thread to finish

        except Exception as e:
            logger.error(f"错误: {str(e)}")
            logger.info("尝试重新连接...")
            time.sleep(RECONNECT_INTERVAL)
        finally:
            try:
                client_socket.close()
            except:
                pass  # Ignore socket close error during reconnection
            logger.info("已断开与服务器的连接...")


if __name__ == '__main__':
    main()
