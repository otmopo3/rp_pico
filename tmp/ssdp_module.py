import network
import socket
import wifi_network_module


def send_broadcast():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    SO_BROADCAST = 32
    s.setsockopt(socket.SOL_SOCKET, SO_BROADCAST, 1)
    
    data = bytes("test", "utf-8")
    s.sendto(data, ("255.255.255.255", 5005))

    print('sent data')

def inet_aton(addr):
        ip_as_bytes = bytes(map(int, addr.split(".")))
        return ip_as_bytes

def send_multicast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    localip = wifi_network_module.get_ip()
    
    membership_data = inet_aton('239.255.255.250') + inet_aton(localip)    
    
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_data)
    sock.bind(('0.0.0.0', 1900))
    
    notify_msg='''
NOTIFY * HTTP/1.1
HOST: 239.255.255.250:1900
CACHE-CONTROL: max-age=300
LOCATION: http://192.168.0.104
OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01
NT: microcontroller:rp2picow
NTS: ssdp:alive
SERVER: rp2pico2
USN: someunique:idscheme3

'''
    
    data = bytes(notify_msg, "utf-8")  
    
    sock.sendto(data, ('239.255.255.250', 1900))
    
    print(notify_msg)



if __name__ == '__main__':

    wifi_network_module.connect_wifi(uri_to_test='')
    print("Connected wifi")
    
    #send_broadcast()
    
    send_multicast()
