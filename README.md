# paddleOCR-Server
A server written in python, based on paddleOCR to detect and recognize text in pictures, based on grpc framework  

一个用python编写的、基于paddleOCR实现检测并识别图片中的文字、基于grpc框架的服务端

## Deployment
After installing dependencies including paddleOCR, and modifying the serverAddress in C_OCRServicer.py, execute:

    python C_OCRServicer.py

安装 paddleOCR 等依赖，并修改 C_OCRServicer.py 中的 serverAddress 后，执行：

    python C_OCRServicer.py
