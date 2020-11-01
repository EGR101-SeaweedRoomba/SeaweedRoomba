import socket

HOST = '10.197.12.245'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data=conn.recv(1024)
            if data and data !=b'GOOBER' and data.find(b'GOO')==-1:
                vals = data.decode()
                print("left: " + str(vals[0:3]) + "\nright: " + str(vals[3:6]))
