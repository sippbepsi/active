## active
## to-do - return the name of the proccess using that port | DONE
## since udp has no handshake, the probing may be inaccurate. this can be remedied by running "sudo" on the script, or running the script with elevated privileges on windows

import socket
import threading
import queue
import time
import psutil
from datetime import datetime

# COLORS, BECAUSE WHY NOT.
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f""" 
    {Colors.CYAN}{Colors.BOLD}╔══════════════════════════╗
    ║ active - a port scanner  ║
    ╚══════════════════════════╝{Colors.ENDC}
    """ # this looks ugly af here. maybe fix this terribleness later
    print(banner)

def get_process_by_port(port, protocol):
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and (
                (protocol == 'TCP' and conn.type == socket.SOCK_STREAM) or
                (protocol == 'UDP' and conn.type == socket.SOCK_DGRAM)
            ):
                try:
                    return psutil.Process(conn.pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return "Unknown"
    except:
        return "Unable to determine :("
    return "No process found :("

def tcp_scan(ip, port, show_process):
    """Scan a single TCP port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = "unknown"
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                pass
            
            process_info = ""
            if show_process:
                process = get_process_by_port(port, 'TCP')
                process_info = f" - {Colors.YELLOW}Process: {process}{Colors.ENDC}"
                
            print(f"{Colors.GREEN}TCP Port {port} ({service}) is open{Colors.ENDC}{process_info}")
        sock.close()
    except:
        pass

def udp_scan(ip, port, show_process):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b'', (ip, port))
        
        try:
            data, addr = sock.recvfrom(1024)
            service = "unknown"
            try:
                service = socket.getservbyport(port, 'udp')
            except:
                pass
                
            process_info = ""
            if show_process:
                process = get_process_by_port(port, 'UDP')
                process_info = f" - {Colors.YELLOW}Process: {process}{Colors.ENDC}"
                
            print(f"{Colors.BLUE}UDP Port {port} ({service}) is open{Colors.ENDC}{process_info}")
        except socket.timeout:
            pass
            
        sock.close()
    except:
        pass

def main():
    print_banner()
    
    # get user input
    target = input(f"{Colors.CYAN}Enter target IP address: {Colors.ENDC}")
    try:
        start_port = int(input(f"{Colors.CYAN}Enter starting port: {Colors.ENDC}"))
        end_port = int(input(f"{Colors.CYAN}Enter ending port: {Colors.ENDC}"))
        show_process = input(f"{Colors.CYAN}Show processes using scanned ports? (y/n): {Colors.ENDC}").lower() == 'y'
    except ValueError:
        print(f"{Colors.RED}Invalid port number{Colors.ENDC}")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print(f"{Colors.RED}Invalid port range! Must be between 1-65535.{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}Scanning {target} from port {start_port} to {end_port}{Colors.ENDC}")
    print(f"{Colors.HEADER}Started at {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}\n")

    port_queue = queue.Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # this is really advanced stuff right here, even minecraft couldn't do it
    threads = []
    max_threads = 100

    while not port_queue.empty():
        if threading.active_count() < max_threads + 1:
            port = port_queue.get()
            
            t = threading.Thread(target=tcp_scan, args=(target, port, show_process))
            threads.append(t)
            t.start()
            
            t = threading.Thread(target=udp_scan, args=(target, port, show_process))
            threads.append(t)
            t.start()
        else:
            time.sleep(0.1)

    for t in threads:
        t.join()

    print(f"\n{Colors.HEADER}Scan completed at - {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")

if __name__ == "__main__":
    main()