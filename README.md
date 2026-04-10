

```markdown
# HARD DDOS v5.0 - ELITE EDITION
### Made By diablocxn

---

## Hakkında

HARD DDOS, çok katmanlı ve yüksek performanslı bir stres testi aracıdır. İçerisinde 10'dan fazla farklı saldırı vektörü barındırır. Çoklu thread desteği sayesinde yüksek bant genişliği ve paket gönderimi sağlar.

---

## Özellikler

| Metod | Açıklama |
|-------|----------|
| SYN Flood | TCP SYN paketleri ile bağlantı havuzunu doldurur |
| UDP Flood | Yüksek boyutlu UDP paketleri ile bant genişliğini tüketir |
| HTTP Flood | GET ve POST istekleri ile web sunucusunu yorar |
| Slowloris | Bağlantıları açık tutarak sunucu kaynaklarını sömürür |
| ICMP Flood | Ping paketleri ile ağ trafiğini şişirir |
| ACK Flood | TCP ACK paketleri ile firewall'ları aşmaya çalışır |
| RST Flood | TCP RST paketleri ile bağlantıları düşürmeye çalışır |
| XMAS Flood | Tüm TCP flag'lerini açarak güvenlik duvarlarını test eder |
| DNS Amplification | DNS sorguları ile amplifikasyon saldırısı yapar |
| NTP Amplification | NTP sunucuları üzerinden amplifikasyon sağlar |
| TCP Connect | Sürekli TCP bağlantısı açarak kaynak tüketir |

---

## Kurulum

### Gereksinimler

- Python 3.6 veya üzeri
- pip3
- git
- Linux (Debian/Ubuntu/Arch) veya macOS
- Root yetkisi (bazı metodlar için)

### Adımlar

```bash
# Repoyu klonla
git clone https://github.com/dixblo-q/HardDDoS

# Dizine gir
cd HardDDoS

# Setup scriptini çalıştır
sudo python3 setup.py
```

Setup scripti otomatik olarak:

· Sistem bağımlılıklarını kurar (libpcap, tcpdump vb.)
· Python kütüphanelerini yükler (scapy, requests vb.)
· Başlatıcı script oluşturur

---

Kullanım

```bash

# Python ile
sudo python3 main.py
```

Ardından sırasıyla:

1. Hedef IP veya hostname girin
2. Hedef portu belirleyin (varsayılan: 80)
3. Paket boyutunu girin (varsayılan: 65535)
4. Süre girin (0 = sonsuz)
5. Thread sayısını belirleyin (varsayılan: 1000)

---

Ekran Görüntüsü

```
🔥 SALDIRI AKTIF Paket: 1,234,567 | Hiz: 45,678 p/s | Bant: 234.56 MB/s | Toplam: 1.2 GB | Sure: 30s
```

---

Sorumluluk Reddi

Bu araç yalnızca aşağıdaki amaçlar için geliştirilmiştir:

· Kendi sunucularınızın dayanıklılığını test etmek
· Yetkili penetrasyon testleri yapmak
· Eğitim ve araştırma faaliyetleri

İzinsiz kullanım:

· Türk Ceza Kanunu Madde 244'e göre suçtur
· 2 yıldan 6 yıla kadar hapis cezası vardır
· Uluslararası siber suç yasalarına aykırıdır

Kullanıcı, aracı kullanarak tüm yasal sorumluluğu üstlenmiş sayılır. Geliştirici hiçbir şekilde sorumlu tutulamaz.

---

Sık Sorulan Sorular

S: Neden root yetkisi gerekiyor?
C: ICMP ve RAW soket işlemleri için sistem düzeyinde yetki gerekir.

S: Windows'ta çalışır mı?
C: Bazı metodlar çalışmaz, Linux önerilir.

S: En etkili metod hangisi?
C: Hedef sisteme göre değişir. SYN + UDP + HTTP kombinasyonu genelde etkilidir.

S: VPN gerekli mi?
C: Kendi güvenliğiniz için şiddetle önerilir.

---

İletişim

· Telegram: t.me/diablocxn

---

Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.

---

Made with ❤️ by diablocxn

```
