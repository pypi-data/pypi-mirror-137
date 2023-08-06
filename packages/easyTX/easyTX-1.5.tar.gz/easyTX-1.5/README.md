# easyTX  (Data_Transfer)

easyTX is the ultimate module to exchange data in any form (video or string) from one PC to another.

Installation
============

    pip install easyTX

The following convention is used here: 
* the server is transmitting data
* the client is receiving data

Usage
============

server_video.py 

    import easyTX.server as server
    server_socket = server.conn('your ip address', 'port no')
    server.frame(server_socket, 0) 

client_video.py

    import cv2
    import easyTX.client as client
    client_socket = client.conn('your ip address', 'port no)
    while True:
        frame = client.frame(client_socket)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        
 server_data.py
 
    import easyTX.server as server
    server_socket = server.conn('your ip address', 'port no)
    while True:
        addr = server.address(server_socket)
        for i in range(0, 10000):
            message = str(i)
            message = message.encode('utf-8')
            server_data.send(server_socket, message, addr)
            
            
client_data.py

    import easyTX.client as client
    client_socket = client.conn('your ip address', 'port no)
    while True:
      data = client.recv(client_socket)
      print(data)
