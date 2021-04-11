import sys
import socket
import headers
import threading

#Send Socket
send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
send_sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)


#Recv Sockets
recv_sock_interface_1 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
recv_sock_interface_1.bind(('ens33', 0))

recv_sock_interface_2 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
recv_sock_interface_2.bind(('ens38', 0))

#Read cmd inputs
inside_local_ip = sys.argv[1]
inside_global_ip = sys.argv[2]

#Recv the traffic from inside interface
def recv_interface_inside():
    while True:
        data = recv_sock_interface_1.recv(65535)
        ip_header = data[14:34]
        IP = headers.IP_Header(ip_header)
        new_packet = data[14:26] + socket.inet_aton(inside_global_ip) + data[30:]
        nat_handler(new_packet, send_sock, IP.dst_address)

#Recv the traffic from outside interface
def recv_interface_outside():
    while True:
        data = recv_sock_interface_2.recv(65535)
        new_packet = data[14:30] + socket.inet_aton(inside_local_ip) + data[34:]
        nat_handler(new_packet, send_sock, inside_local_ip)
       
#Send the packet
def nat_handler(packet, socket, dst_ip):
    socket.sendto(packet, (dst_ip , 0 ))


#Thread the traffic recving funtions to execute simultaneously
int1_thread = threading.Thread(target=recv_interface_inside, args=() )
int2_thread = threading.Thread(target=recv_interface_outside, args=() )

int1_thread.start()
int2_thread.start()


