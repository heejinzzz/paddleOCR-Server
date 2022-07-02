import grpc
from concurrent import futures
import C_OCR_pb2_grpc
import C_OCR_pb2
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import struct

serverAddress = "127.0.0.1:8700"


class C_OCRServicer(C_OCR_pb2_grpc.C_OCRServicer):
    def __init__(self):
        self.ocr = PaddleOCR(use_angle=True, lang="ch")

    def Ocr(self, request, context):
        img_name = "./origin_img." + request.ImageType
        img_bytes = request.ImageBytes
        img_file = open(img_name, "wb")
        for i in img_bytes:
            s = struct.pack('B', i)
            img_file.write(s)
        img_file.close()

        result = self.ocr.ocr(img_name)
        text = ""
        for line in result:
            text = text + line[1][0] + "\n"

        image = Image.open(img_name).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        result_img = draw_ocr(image, boxes, txts, scores, font_path="./fonts/simhei.ttf")
        result_img = Image.fromarray(result_img)
        result_img_name = "./result_img."+request.ImageType
        result_img.save(result_img_name)

        result_img_file = open(result_img_name, "rb")
        result_img_bytes = result_img_file.read()
        result_img_bytes = bytes(struct.unpack("B"*len(result_img_bytes), result_img_bytes))
        result_img_file.close()

        response = C_OCR_pb2.Response(Text=text, ImageBytes=result_img_bytes)
        return response


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    C_OCR_pb2_grpc.add_C_OCRServicer_to_server(C_OCRServicer(), server)
    server.add_insecure_port(serverAddress)
    server.start()
    server.wait_for_termination()
