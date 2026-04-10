#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HARD DDOS - Setup Script
Made By diablocxn
"""

import os
import sys
import subprocess
import platform
import shutil
import time

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

def print_banner():
    banner = f"""
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
║                    {YELLOW}⚡ SETUP & INSTALLATION SCRIPT ⚡{RED}                    ║
║                         {WHITE}Made By diablocxn{RED}                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)

def print_step(message):
    print(f"{CYAN}[+]{RESET} {message}")

def print_success(message):
    print(f"{GREEN}[✓]{RESET} {message}")

def print_error(message):
    print(f"{RED}[✗]{RESET} {message}")

def print_warning(message):
    print(f"{YELLOW}[!]{RESET} {message}")

def print_info(message):
    print(f"{BLUE}[i]{RESET} {message}")

def check_root():
    """Root yetkisi kontrolü"""
    if os.geteuid() != 0:
        print_warning("Bu script root yetkisi ile çalıştırılmıyor!")
        print_info("Bazı bağımlılıklar için root gerekebilir.")
        print_info("Devam etmek için ENTER, iptal için Ctrl+C")
        input()
    else:
        print_success("Root yetkisi: EVET")

def check_os():
    """İşletim sistemi kontrolü"""
    os_name = platform.system()
    if os_name == "Linux":
        print_success(f"İşletim Sistemi: {os_name} - Destekleniyor")
        return "linux"
    elif os_name == "Darwin":
        print_warning(f"İşletim Sistemi: macOS - Kısmi destek")
        return "macos"
    else:
        print_error(f"İşletim Sistemi: {os_name} - Desteklenmiyor!")
        return "unsupported"

def check_python_version():
    """Python versiyon kontrolü"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print_success(f"Python Versiyonu: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python Versiyonu: {version.major}.{version.minor}.{version.micro} - Python 3.6+ gerekli!")
        return False

def run_command(command, shell=False):
    """Komut çalıştır"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_pip():
    """Pip kurulumu"""
    print_step("Pip kontrol ediliyor...")
    
    success, stdout, stderr = run_command("pip3 --version")
    if success:
        print_success("Pip zaten kurulu")
        return True
    
    success, stdout, stderr = run_command("pip --version")
    if success:
        print_success("Pip zaten kurulu")
        return True
    
    print_warning("Pip kurulu değil, kuruluyor...")
    
    os_name = platform.system()
    if os_name == "Linux":
        # Debian/Ubuntu
        success, _, _ = run_command("apt-get update", shell=True)
        success, _, _ = run_command("apt-get install -y python3-pip", shell=True)
        
        # RHEL/CentOS
        if not success:
            success, _, _ = run_command("yum install -y python3-pip", shell=True)
        
        # Arch
        if not success:
            success, _, _ = run_command("pacman -S --noconfirm python-pip", shell=True)
    
    elif os_name == "Darwin":
        success, _, _ = run_command("easy_install pip", shell=True)
    
    if success:
        print_success("Pip başarıyla kuruldu")
        return True
    else:
        print_error("Pip kurulamadı!")
        return False

def install_system_dependencies(os_type):
    """Sistem bağımlılıklarını kur"""
    print_step("Sistem bağımlılıkları kuruluyor...")
    
    if os_type == "linux":
        # Tespit et dağıtım
        distro = ""
        if os.path.exists("/etc/debian_version"):
            distro = "debian"
        elif os.path.exists("/etc/redhat-release"):
            distro = "redhat"
        elif os.path.exists("/etc/arch-release"):
            distro = "arch"
        
        packages = [
            "python3-dev",
            "python3-setuptools",
            "build-essential",
            "libpcap-dev",
            "tcpdump",
            "net-tools",
            "iproute2",
            "libssl-dev",
            "libffi-dev",
            "git",
            "curl",
            "wget"
        ]
        
        if distro == "debian":
            print_info("Debian/Ubuntu tabanlı sistem tespit edildi")
            cmd = f"apt-get install -y {' '.join(packages)}"
            run_command("apt-get update", shell=True)
            run_command(cmd, shell=True)
            
        elif distro == "redhat":
            print_info("RHEL/CentOS tabanlı sistem tespit edildi")
            packages = [
                "python3-devel",
                "gcc",
                "libpcap-devel",
                "tcpdump",
                "net-tools",
                "openssl-devel",
                "libffi-devel",
                "git",
                "curl",
                "wget"
            ]
            cmd = f"yum install -y {' '.join(packages)}"
            run_command(cmd, shell=True)
            
        elif distro == "arch":
            print_info("Arch Linux tabanlı sistem tespit edildi")
            packages = [
                "python",
                "python-pip",
                "base-devel",
                "libpcap",
                "tcpdump",
                "net-tools",
                "iproute2",
                "openssl",
                "libffi",
                "git",
                "curl",
                "wget"
            ]
            cmd = f"pacman -S --noconfirm {' '.join(packages)}"
            run_command(cmd, shell=True)
        
        print_success("Sistem bağımlılıkları kuruldu")
    
    elif os_type == "macos":
        print_info("macOS tespit edildi")
        
        # Homebrew kontrol
        success, _, _ = run_command("brew --version")
        if not success:
            print_warning("Homebrew kurulu değil, kuruluyor...")
            run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)
        
        packages = [
            "python3",
            "libpcap",
            "openssl",
            "libffi"
        ]
        
        for pkg in packages:
            run_command(f"brew install {pkg}", shell=True)
        
        print_success("macOS bağımlılıkları kuruldu")

def install_python_packages():
    """Python paketlerini kur"""
    print_step("Python paketleri kuruluyor...")
    
    packages = [
        "scapy>=2.4.5",
        "requests>=2.28.0",
        "urllib3>=1.26.0",
        "colorama>=0.4.6",
        "cryptography>=38.0.0",
        "pyOpenSSL>=22.0.0",
        "certifi>=2022.0.0",
    ]
    
    # Pip güncelle
    run_command("pip3 install --upgrade pip", shell=True)
    
    # Ana paketleri kur
    for package in packages:
        print_info(f"Kuruluyor: {package}")
        success, stdout, stderr = run_command(f"pip3 install {package}", shell=True)
        
        if success:
            print_success(f"Kuruldu: {package}")
        else:
            print_error(f"Kurulamadı: {package}")
            print_info(f"Hata: {stderr[:100]}")
    
    print_success("Python paketleri kurulumu tamamlandı")

def create_launcher():
    """Başlatıcı script oluştur"""
    print_step("Başlatıcı oluşturuluyor...")
    
    launcher_content = """#!/bin/bash
# HARD DDOS Launcher
# Made By diablocxn

cd "$(dirname "$0")"

if [ "$EUID" -ne 0 ]; then 
    echo "[!] Root yetkisi gerekli!"
    echo "[+] Sudo ile çalıştırılıyor..."
    sudo python3 hard_ddos.py "$@"
else
    python3 hard_ddos.py "$@"
fi
"""
    
    with open("hard_ddos.sh", "w") as f:
        f.write(launcher_content)
    
    os.chmod("hard_ddos.sh", 0o755)
    print_success("Başlatıcı oluşturuldu: hard_ddos.sh")

def create_requirements():
    """Requirements.txt oluştur"""
    print_step("Requirements.txt oluşturuluyor...")
    
    requirements = """scapy>=2.4.5
requests>=2.28.0
urllib3>=1.26.0
colorama>=0.4.6
cryptography>=38.0.0
pyOpenSSL>=22.0.0
certifi>=2022.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print_success("requirements.txt oluşturuldu")

def check_network():
    """Ağ bağlantısı kontrolü"""
    print_step("Ağ bağlantısı kontrol ediliyor...")
    
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print_success("İnternet bağlantısı: AKTİF")
        return True
    except:
        print_warning("İnternet bağlantısı yok! Bazı kurulumlar başarısız olabilir.")
        return False

def create_desktop_entry():
    """Masaüstü kısayolu oluştur (Linux)"""
    if platform.system() != "Linux":
        return
    
    print_step("Masaüstü kısayolu oluşturuluyor...")
    
    desktop_entry = f"""[Desktop Entry]
Name=HARD DDOS
Comment=DDoS Attack Tool - Made By diablocxn
Exec={os.path.abspath('hard_ddos.sh')}
Icon={os.path.abspath('icon.png')}
Terminal=true
Type=Application
Categories=Network;Security;
"""
    
    desktop_path = os.path.expanduser("~/.local/share/applications/hard_ddos.desktop")
    os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
    
    with open(desktop_path, "w") as f:
        f.write(desktop_entry)
    
    print_success(f"Masaüstü kısayolu oluşturuldu: {desktop_path}")

def verify_installation():
    """Kurulumu doğrula"""
    print_step("Kurulum doğrulanıyor...")
    
    all_ok = True
    
    # Python paketlerini kontrol et
    packages = ["scapy", "requests", "urllib3"]
    
    for package in packages:
        try:
            __import__(package)
            print_success(f"{package} modülü: YÜKLÜ")
        except ImportError:
            print_error(f"{package} modülü: YÜKLÜ DEĞİL")
            all_ok = False
    
    return all_ok

def print_completion():
    """Kurulum tamamlandı mesajı"""
    completion = f"""
{GREEN}{BOLD}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                         ✅ KURULUM TAMAMLANDI! ✅                       ║
║                                                                       ║
║                         HARD DDOS - Made By diablocxn                  ║
║                                                                       ║
║  {WHITE}Kullanım:{GREEN}                                                          ║
║     ./hard_ddos.sh          - Başlatıcı ile çalıştır                 ║
║     sudo python3 main.py  - Direkt Python ile çalıştır                ║
║                                                                       ║
║  {WHITE}Özellikler:{GREEN}                                                       ║
║     • SYN Flood              • UDP Flood                              ║
║     • HTTP Flood             • Slowloris                              ║
║     • ICMP Flood             • ACK/RST/XMAS Flood                     ║
║     • DNS Amplification      • NTP Amplification                      ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{RESET}
{RED}{BOLD}⚠️  UYARI: Bu araç sadece YETKİLİ sistemlerde kullanılmalıdır!{RESET}
{RED}     İzinsiz kullanım SUÇTUR ve ağır cezaları vardır.{RESET}
    """
    print(completion)

def main():
    """Ana kurulum fonksiyonu"""
    print_banner()
    
    print(f"{CYAN}{'═'*70}{RESET}")
    print(f"{WHITE}{BOLD}SİSTEM KONTROLLERİ{RESET}")
    print(f"{CYAN}{'═'*70}{RESET}\n")
    
    # Sistem kontrolleri
    os_type = check_os()
    if os_type == "unsupported":
        print_error("Desteklenmeyen işletim sistemi!")
        sys.exit(1)
    
    if not check_python_version():
        print_error("Python 3.6+ gerekli!")
        sys.exit(1)
    
    check_root()
    
    print(f"\n{CYAN}{'═'*70}{RESET}")
    print(f"{WHITE}{BOLD}BAĞIMLILIK KURULUMU{RESET}")
    print(f"{CYAN}{'═'*70}{RESET}\n")
    
    # İnternet kontrolü
    check_network()
    
    # Pip kurulumu
    if not install_pip():
        print_error("Pip kurulamadı! Manuel kurun.")
        sys.exit(1)
    
    # Sistem bağımlılıkları
    if os.geteuid() == 0:
        install_system_dependencies(os_type)
    else:
        print_warning("Sistem bağımlılıkları için root gerekli, atlanıyor...")
    
    # Python paketleri
    install_python_packages()
    
    print(f"\n{CYAN}{'═'*70}{RESET}")
    print(f"{WHITE}{BOLD}YAPILANDIRMA{RESET}")
    print(f"{CYAN}{'═'*70}{RESET}\n")
    
    # Dosyaları oluştur
    create_requirements()
    create_launcher()
    
    if os_type == "linux" and os.geteuid() == 0:
        create_desktop_entry()
    
    print(f"\n{CYAN}{'═'*70}{RESET}")
    print(f"{WHITE}{BOLD}DOĞRULAMA{RESET}")
    print(f"{CYAN}{'═'*70}{RESET}\n")
    
    # Kurulumu doğrula
    if verify_installation():
        print_success("Tüm bileşenler başarıyla kuruldu!")
    else:
        print_warning("Bazı bileşenler kurulamadı, manuel kurulum gerekebilir.")
    
    print_completion()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Kurulum iptal edildi.{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Beklenmeyen hata: {e}")
        sys.exit(1)
