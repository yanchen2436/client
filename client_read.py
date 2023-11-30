import socket
import threading
import subprocess
import os
import time
import logging
import re
import netifaces

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


def parse_value(output):
    # 用正则表达式从输出中提取参数值
    match = re.search(r'(?<=\s)(0x[0-9a-f]+|[0-9.]+)(?=\s|$)', output)
    if match:
        value = match.group()
        if value.startswith("0x"):
            value = value[2:]  # 去掉前缀 "0x"
        return value
    return ""


def get_local_ip():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            iface_details = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in iface_details:
                ip_info = iface_details[netifaces.AF_INET][0]
                if 'addr' in ip_info and not ip_info['addr'].startswith('127.'):
                    return ip_info['addr'].split('.')[-1][-1]
        return None
    except (socket.error, ValueError, IndexError):
        return None

local_last_octet = get_local_ip()
print(local_last_octet)


def get_camera_params(script_path, camnum):
    ipnum = get_local_ip()
    params = {'camnum': str(ipnum) + str(camnum)}
    expmode_output = subprocess.getoutput(f"{script_path} -b {camnum} -r -f expmode")
    params['expmode'] = parse_value(expmode_output)
    metime_output = subprocess.getoutput(f"{script_path} -b {camnum} -r -f metime")
    params['metime'] = parse_value(metime_output)
    meagain_output = subprocess.getoutput(f"{script_path} -b {camnum} -r -f meagain")
    params['meagain'] = parse_value(meagain_output)
    medgain_output = subprocess.getoutput(f"{script_path} -b {camnum} -r -f medgain")
    params['medgain'] = parse_value(medgain_output)
    imagedir_output = subprocess.getoutput(f"{script_path} -b {camnum} -r -f imagedir")
    params['imagedir'] = parse_value(imagedir_output)

    return params


def parse_and_execute(json_data, script_path, client_socket):
    import json
    global proc  # 使用全局的proc变量
    target_directory = os.path.dirname(script_path)
    
    # 确保json_data是一个非空列表
    if json_data and isinstance(json_data, list):
        # 遍历json_data列表中的每个字典
        for item in json_data:
            # 获取字典中的各项值
            camnum = item.get('camnum', '')
            expmode = item.get('expmode', '')
            imageDir = item.get('imageDir', '')
            meagain = item.get('meagain', '')
            medgain = item.get('medgain', '')
            metime = item.get('metime', '')
            msg = item.get('msg', '')
            returnip = item.get('returnip', '')

        # 切换到目标目录
        os.chdir(target_directory)
        # logger.info("开始解析和执行")
        if msg == "0x00":
            # logger.debug("开启激光")
            # subprocess.run(["python3", "/home/nano/client/open.py"])
            logger.debug("0x00")
            # proc = subprocess.Popen(["python3", "/home/nano/client/csave.py"])

        elif msg == "0xff":
            # if proc is not None:
            #    proc.terminate()
            logger.debug("0xff")
            #    proc = None
            # subprocess.run(["python3", "/home/nano/client/close.py"])
            # logger.debug("关闭激光")

        elif msg == "0x03":
            logger.debug("0x03")
            # subprocess.run(["python3", "/home/nano/client/open.py"])

        elif msg == "0x04":
            logger.debug("0x04")
            # subprocess.run(["python3", "/home/nano/client/close.py"])

        elif msg == "0xfe":
            # 在收到消息 "0x05" 时运行 get_camera_params 并将结果打印到控制台
            params0 = get_camera_params(script_path, 7)
            params1 = get_camera_params(script_path, 8)
            data_to_send_params0 = {
                returnip: [params0, params1]
            }
            # data_to_send_params1 = {
            #     returnip: [params1]
            # }
            json_data_to_send_params0 = json.dumps(data_to_send_params0)
            # json_data_to_send_params1 = json.dumps(data_to_send_params1)
            client_socket.send(json_data_to_send_params0.encode('utf-8'))
            # client_socket.send(json_data_to_send_params1.encode('utf-8'))
            print("Camera Parameters:", data_to_send_params0)
            # print("Camera Parameters:", data_to_send_params1)

        elif msg == "0x06":
            # 当消息为 "0x06" 时执行这些命令
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
        # logger.info("解析和执行完成")
        # logger.debug(params)


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
                parse_and_execute(json_data, script_path, client_socket)



        except Exception as e:
            print("Error while receiving message:", str(e))
            break


def main():
    server_ip = '192.168.10.107'
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
