# python 3.x
# coding= utf-8

import sys
import socket
import argparse
from threading import *

## Semaphore needed for printing stuff on screen
screenLock = Semaphore(value=1)

# true if the -v or --verbose option is given
# indicates that the program must talk more
verbose = False

# get the banner of the service running
# at the given IP/Port couple
def grabBanner(ip, port):
    soc = None
    try:
        # creation of the socket
        socket.setdefaulttimeout(3)     # 3 sec of timeout. Think about making it a param
        soc = socket.socket()

        if(verbose):
            screenLock.acquire()
            print("[+] Connecting to ", ip, " port ", str(port))

        soc.connect((ip, port))

        # here we get the banner of the service runnning
        banner = soc.recv(1024)

        # display of the banner and the port associated
        screenLock.acquire()
        print("[+] ", port, " ==> ", banner)

    except Exception as e:
        if(verbose):
            screenLock.acquire()
            print("[E] ", str(e))
            print("[E] Port ", port, " : Impossible to fetch the banner !")
    finally:
        soc.close()
        screenLock.release()


def main():
    ## parsing parameters
    parser = argparse.ArgumentParser("Simple banner grabber")
    parser.add_argument('hostAddress', help="IP address of the target host", type=str)
    parser.add_argument('port_str', nargs='?', default="21,22,23,80", help="Port list separated by \',\' or \'-\' for ranges")
    parser.add_argument('-v', '--verbose', help="Verbose output", action='store_true')
    params = parser.parse_args()

    hostAddress = params.hostAddress
    verbose = params.verbose

    # the port string must be parsed
    port_list = []
    for port in params.port_str.split(','):
        if '-' in port: # allows port ranges
            interval = port.split('-')
            for i in range(int(interval[0]), int(interval[1])+1):
                port_list.append(i);
        else:
            port_list.append(port)

    print("Target host : ", hostAddress)

    for port in port_list:         # lets connect to each port !
        t = Thread(target=grabBanner, args=(hostAddress, port))
        t.start()

    print("Terminated")

if __name__ == "__main__":
    main()
