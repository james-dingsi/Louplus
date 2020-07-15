import sys
import socket

def get_arg():
    arg = sys.argv[1:]

    try:
        host_arg = arg[arg.index('--host') + 1]
        port_arg = arg[arg.index('--port') + 1]
    
        if len(host_arg.split('.')) != 4:
            raise ValueError
        else:
            for v in host_arg.split('.'):
                if int(v) >= 255:
                    raise ValueError
            host =host_arg
            
        if len(port_arg.split('-')) == 2:
            port_list = port_arg.split('-')
            port = [int(port_list[0]), int(port_list[1])]
        else:
            port = [int(port_arg), int(port_arg)]
        return host, port
    except:
        print('Parameter Error')
        exit()   

def scan():
    host, port = get_arg()
    open_list =[]
    for i in range(port[0], port[1] + 1):
        s = socket.socket()
        s.settimeout(0.2)
        if s.connect_ex((host, i)) == 0:
            print(i, 'open')
            open_list.append(i)
        else: 
            print(i, 'close')
        s.close()
    


if __name__ == '__main__':
    scan()

    