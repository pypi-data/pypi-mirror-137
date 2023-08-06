import cv2, socket
import numpy as np
import time
import base64
BUFF_SIZE = 65536

def conn(host_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    client_socket.sendto(f'Client GOT Connection: {(host_ip, port)}'.encode('utf-8'), (host_ip, port))
    return client_socket

def frame(client_socket):
    """Loop."""
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.fromstring(data, dtype = np.uint8)
    frame = cv2.imdecode(npdata, 1)
    return frame
        
def recv(client_socket):
    """Loop."""
    packet, _ = client_socket.recvfrom(65535)
    data = packet.decode('utf-8')
    return data
