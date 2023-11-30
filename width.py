import cv2
import argparse

def main():
    parser = argparse.ArgumentParser(description="Display a video stream with optional cropping.")
    parser.add_argument("-width", nargs=2, type=int, help="Specify the width range for cropping (e.g., -width 500 800)")
    args = parser.parse_args()

    # 打开摄像头
    cap = cv2.VideoCapture(1)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # 设置摄像头的分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while True:
        # 读取视频帧
        ret, frame = cap.read()

        if ret:
            # 如果指定了宽度范围，则进行裁剪
            if args.width:
                start_width, end_width = args.width
                frame = frame[:, start_width:end_width, :]

            # 显示视频帧
            cv2.imshow("Video", frame)

        # 检查是否按下了 ESC 键
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
