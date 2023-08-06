import cv2, imutils, socket
import base64


BUFF_SIZE = 65536
def conn(host_ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    print('Listening at:', socket_address)
    return server_socket

def frame(server_socket, source, width = 400):
    vid = cv2.VideoCapture(source) 
    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        print(msg)
        while vid.isOpened():
            _, frame = vid.read()
            if _:
                frame = imutils.resize(frame, width = width)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                message = base64.b64encode(buffer)
                server_socket.sendto(message, client_addr)
            else:
                print('no video')
                vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
   
def address(server_socket):
    """Loop."""
    msg, addr = server_socket.recvfrom(65535)
    print('GOT: ', addr)
    return addr

def send(server_socket, message, addr):
    server_socket.sendto(message, addr)   
