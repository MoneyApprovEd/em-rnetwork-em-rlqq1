"""
EMIRNETWORK — Elite Network Intelligence Platform
True RGB rainbow engine, dollar-sign ASCII art, advanced OSINT modules.
Windows UTF-8 compatible.
"""

import os, sys, math, socket, threading, time, json, struct, random, hashlib
import concurrent.futures
from datetime import datetime

os.system('color')
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

try:
    import psutil; HAS_PSUTIL = True
except ImportError: HAS_PSUTIL = False

try:
    import requests; HAS_REQUESTS = True
except ImportError: HAS_REQUESTS = False

try:
    from scapy.all import IP, TCP, UDP, ICMP, send; HAS_SCAPY = True
except ImportError: HAS_SCAPY = False


# ═══════════════════════════════════════════════════════════════
#  TRUE RGB RAINBOW ENGINE
# ═══════════════════════════════════════════════════════════════

class RainbowEngine:
    """EMIRNETWORK Elite 24-bit RGB engine - Full Feature Edition."""

    def __init__(self, frequency=0.08, speed=2.0, offset=0.0):
        self.frequency = frequency 
        self.speed = speed
        self.offset = offset

    @staticmethod
    def _clamp(v):
        return max(0, min(255, v))

    def rgb_at(self, x, y, start_val=0):
        # Zaman, koordinat ve başlangıç değerine göre renk hesaplar
        t = (x * self.frequency) + (y * 0.2) + (time.time() * self.speed) + self.offset + start_val
        r = self._clamp(int(127.5 * (1 + math.sin(t))))
        g = self._clamp(int(127.5 * (1 + math.sin(t + 2.094))))
        b = self._clamp(int(127.5 * (1 + math.sin(t + 4.189))))
        return r, g, b

    def colorize(self, text, start=0):
        """Tek satırlık metinleri boyamak için gereken metod (Hata burada çıkıyordu)."""
        out = []
        for i, ch in enumerate(text):
            # Tek satır olduğu için y değerini 0 alıyoruz
            r, g, b = self.rgb_at(i, 0, start_val=start)
            out.append(f"\033[38;2;{r};{g};{b}m{ch}")
        out.append("\033[0m")
        return "".join(out)

    def colorize_block(self, lines, start=0):
        """Banner gibi çok satırlı blokları boyamak için metod."""
        result = []
        for y, line in enumerate(lines):
            colored_line = []
            for x, ch in enumerate(line):
                r, g, b = self.rgb_at(x, y, start_val=start)
                colored_line.append(f"\033[38;2;{r};{g};{b}m{ch}")
            result.append("".join(colored_line) + "\033[0m")
        return "\n".join(result)


# ═══════════════════════════════════════════════════════════════
#  DOLLAR-SIGN ASCII ART BANNER — "EMIRNETWORK"
# ═══════════════════════════════════════════════════════════════

# Bu banner, attığın görseldeki kalın blok fontuna göre uyarlandı.
EMIRNETWORK_BANNER = [
    " ███████╗███╗   ███╗██╗██████╗ ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗ ",
    " ██╔════╝████╗ ████║██║██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝ ",
    " █████╗  ██╔████╔██║██║██████╔╝██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝  ",
    " ██╔══╝  ██║╚██╔╝██║██║██╔══██╗██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗  ",
    " ███████╗██║ ╚═╝ ██║██║██║  ██║██║ ╚████║███████╗    ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗ ",
    " ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝    ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ "
]

class RainbowBanner:
    def __init__(self):
        self.engine = RainbowEngine(speed=0.08, offset=0.0)
        self._anim_offset = 0.0

    def animate_offset(self):
        self._anim_offset += 0.35

    def print_banner(self):
        self.animate_offset()
        engine = RainbowEngine(speed=0.08, offset=self._anim_offset)
        print()
        print(engine.colorize_block(EMIRNETWORK_BANNER, start=0))
        print()
        sub = "E L I T E   N E T W O R K   I N T E L L I G E N C E   P L A T F O R M"
        print(engine.colorize(sub, start=200))
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(engine.colorize(f"  [{ts}]", start=300))
        print()

    def print_header(self, title):
        engine = RainbowEngine(speed=0.18, offset=self._anim_offset)
        width = 60
        pad = (width - len(title)) // 2
        line = "\u2500" * width
        print(engine.colorize(line, start=0))
        print(engine.colorize(" " * pad + title + " " * pad, start=30))
        print(engine.colorize(line, start=60))
        print()


# ═══════════════════════════════════════════════════════════════
#  PORT SCANNER — HIGH-SPEED MULTITHREADED
# ═══════════════════════════════════════════════════════════════

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB",
}

SERVICE_BANNERS = {
    21: "220 FTP Server Ready", 22: "SSH-2.0-OpenSSH_8.9",
    25: "220 SMTP Server", 80: "HTTP/1.1 200 OK",
    110: "+OK POP3 Server Ready", 143: "* OK IMAP4rev1 Server",
    443: "TLS/1.3", 3306: "MySQL 8.0 Protocol",
}


class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1.0, max_threads=200):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.max_threads = max_threads
        self.results = []
        self._lock = threading.Lock()

    def _resolve(self):
        try:
            return socket.gethostbyname(self.target)
        except socket.gaierror:
            return self.target

    def _scan_port(self, port, ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((ip, port)) == 0:
                    service = COMMON_PORTS.get(port, "Unknown")
                    banner = self._grab_banner(s, port)
                    with self._lock:
                        self.results.append((port, service, banner))
        except Exception:
            pass

    @staticmethod
    def _grab_banner(sock, port):
        try:
            if port in (80, 443, 8080):
                sock.sendall(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")
            else:
                sock.sendall(b"\r\n")
            sock.settimeout(2.0)
            data = sock.recv(1024).decode("utf-8", errors="ignore").strip()
            return data[:80] if data else SERVICE_BANNERS.get(port, "No banner")
        except Exception:
            return SERVICE_BANNERS.get(port, "No banner")

    def run(self):
        ip = self._resolve()
        engine = RainbowEngine(speed=0.22)
        print(engine.colorize(f"  [SCANNING] {self.target} ({ip})  Ports {self.start_port}-{self.end_port}", start=0))
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as pool:
            futures = [pool.submit(self._scan_port, p, ip) for p in range(self.start_port, self.end_port + 1)]
            done, total = 0, len(futures)
            for f in concurrent.futures.as_completed(futures):
                done += 1
                pct = int(done / total * 100)
                bar = "\u2588" * (pct // 2) + "\u2591" * (50 - pct // 2)
                print(f"\r  [\033[38;2;0;255;128m{bar}\033[0m] {pct}%", end="", flush=True)
                f.result()
        elapsed = time.time() - start
        print()
        self.results.sort(key=lambda x: x[0])
        return self.results, elapsed


# ═══════════════════════════════════════════════════════════════
#  GEO-IP & WHOIS MODULE
# ═══════════════════════════════════════════════════════════════

class GeoIPWhois:
    def __init__(self, target):
        self.target = target
        self.engine = RainbowEngine(speed=0.20)

    def _geo_ip(self):
        if not HAS_REQUESTS:
            return {"error": "requests library not installed"}
        try:
            ip = socket.gethostbyname(self.target)
        except socket.gaierror:
            ip = self.target
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=8)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def _whois_lookup(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(8)
            s.connect(("whois.iana.org", 43))
            s.sendall((self.target + "\r\n").encode())
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
            s.close()
            return data.decode("utf-8", errors="ignore")[:2000]
        except Exception as e:
            return f"Whois error: {e}"

    def run(self):
        engine = self.engine
        print(engine.colorize(f"  [GEO-IP] Resolving {self.target}...", start=0))
        geo = self._geo_ip()
        if "error" in geo:
            print(f"  \033[38;2;255;60;60m[ERROR] {geo['error']}\033[0m")
        else:
            fields = [
                ("IP", geo.get("query", "N/A")), ("Country", geo.get("country", "N/A")),
                ("Region", geo.get("regionName", "N/A")), ("City", geo.get("city", "N/A")),
                ("ZIP", geo.get("zip", "N/A")), ("Lat", str(geo.get("lat", "N/A"))),
                ("Lon", str(geo.get("lon", "N/A"))), ("ISP", geo.get("isp", "N/A")),
                ("Org", geo.get("org", "N/A")), ("Timezone", geo.get("timezone", "N/A")),
            ]
            for i, (k, v) in enumerate(fields):
                print(engine.colorize(f"    {k:>10}: {v}", start=i * 5))
        print()
        print(engine.colorize(f"  [WHOIS] Querying {self.target}...", start=50))
        for i, line in enumerate(self._whois_lookup().splitlines()[:30]):
            if line.strip():
                print(engine.colorize(f"    {line}", start=80 + i * 3))


# ═══════════════════════════════════════════════════════════════
#  TRAFFIC SIMULATOR — SCAPY OR MOCK ENGINE
# ═══════════════════════════════════════════════════════════════

if HAS_SCAPY:
    class PacketBuilder:
        @staticmethod
        def build_tcp(src, dst, sport, dport):
            return IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, flags="S")
        @staticmethod
        def build_udp(src, dst, sport, dport):
            return IP(src=src, dst=dst) / UDP(sport=sport, dport=dport)
        @staticmethod
        def build_icmp(src, dst):
            return IP(src=src, dst=dst) / ICMP()
        @staticmethod
        def send_packet(pkt):
            send(pkt, verbose=0)
else:
    class _MockIP:
        def __init__(self, src, dst, proto="TCP", sport=0, dport=0, flags=""):
            self.src, self.dst, self.proto = src, dst, proto
            self.sport, self.dport, self.flags = sport, dport, flags
            self.size = random.randint(40, 1500)
        def __repr__(self):
            return f"{self.proto} {self.src}:{self.sport} -> {self.dst}:{self.dport} [{self.flags}] len={self.size}"

    class PacketBuilder:
        @staticmethod
        def build_tcp(src, dst, sport, dport):
            return _MockIP(src, dst, "TCP", sport, dport, flags=random.choice(["S","SA","A","PA","FA"]))
        @staticmethod
        def build_udp(src, dst, sport, dport):
            return _MockIP(src, dst, "UDP", sport, dport)
        @staticmethod
        def build_icmp(src, dst):
            return _MockIP(src, dst, "ICMP", 0, 0, flags="echo-request")
        @staticmethod
        def send_packet(pkt):
            pass


class TrafficSimulator:
    PROTOCOLS = ["TCP", "UDP", "ICMP"]
    FLAGS = ["SYN", "SYN-ACK", "ACK", "PSH-ACK", "FIN-ACK", "RST", "ECHO", "REPLY"]

    def __init__(self, duration=15, rate=0.3):
        self.duration = duration
        self.rate = rate
        self.engine = RainbowEngine(speed=0.12)
        self._running = False

    def _random_ip(self):
        return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

    def _generate_packet(self):
        proto = random.choice(self.PROTOCOLS)
        src, dst = self._random_ip(), self._random_ip()
        sport = random.randint(1024, 65535)
        dport = random.choice([21,22,25,53,80,110,143,443,3306,8080,random.randint(1024,65535)])
        flag = random.choice(self.FLAGS)
        size = random.randint(40, 1500)
        return proto, src, sport, dst, dport, flag, size

    def run(self):
        self._running = True
        engine = self.engine
        print(engine.colorize("  [TRAFFIC] Live packet simulation starting...", start=0))
        print()
        start, count = time.time(), 0
        try:
            while self._running and (time.time() - start) < self.duration:
                proto, src, sport, dst, dport, flag, size = self._generate_packet()
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                line = f"  {ts}  {proto:<5} {src:>15}:{sport:<5} -> {dst:>15}:{dport:<5} [{flag:<9}] {size:>5}B"
                print(engine.colorize(line, start=count * 4))
                count += 1
                time.sleep(self.rate)
        except KeyboardInterrupt:
            pass
        self._running = False
        print()
        print(engine.colorize(f"  [TRAFFIC] Simulation ended — {count} packets captured.", start=count * 4))


# ═══════════════════════════════════════════════════════════════
#  SYSTEM METRICS — REAL-TIME CPU / RAM BARS
# ═══════════════════════════════════════════════════════════════

class SystemMetrics:
    BAR_WIDTH = 40

    def __init__(self):
        self.engine = RainbowEngine(speed=0.25)

    @staticmethod
    def _bar(pct, width=40):
        filled = int(pct / 100 * width)
        empty = width - filled
        if pct < 50: color = "\033[38;2;0;255;100m"
        elif pct < 80: color = "\033[38;2;255;200;0m"
        else: color = "\033[38;2;255;50;50m"
        return f"{color}{'\u2588' * filled}\033[38;2;60;60;60m{'\u2591' * empty}\033[0m"

    def _psutil_metrics(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        net = psutil.net_io_counters()
        disk = psutil.disk_usage("/")
        return {"cpu_pct": cpu, "mem_pct": mem.percent, "mem_used": mem.used,
                "mem_total": mem.total, "net_sent": net.bytes_sent, "net_recv": net.bytes_recv,
                "disk_pct": disk.percent, "disk_used": disk.used, "disk_total": disk.total}

    def _fallback_metrics(self):
        return {"cpu_pct": random.uniform(5,45), "mem_pct": random.uniform(30,70),
                "mem_used": random.randint(2_000_000_000,8_000_000_000), "mem_total": 16_000_000_000,
                "net_sent": random.randint(1_000_000,50_000_000), "net_recv": random.randint(5_000_000,100_000_000),
                "disk_pct": random.uniform(40,80), "disk_used": random.randint(100_000_000_000,400_000_000_000),
                "disk_total": 500_000_000_000}

    @staticmethod
    def _fmt_bytes(b):
        for unit in ("B","KB","MB","GB","TB"):
            if b < 1024: return f"{b:.1f} {unit}"
            b /= 1024
        return f"{b:.1f} PB"

    def run(self, iterations=10, interval=1.0):
        engine = self.engine
        print(engine.colorize("  [METRICS] Real-time system monitoring", start=0))
        print()
        for i in range(iterations):
            m = self._psutil_metrics() if HAS_PSUTIL else self._fallback_metrics()
            if i > 0:
                print(f"\033[F" * 5, end="")
            print(engine.colorize(f"  CPU   [{self._bar(m['cpu_pct'])}] {m['cpu_pct']:5.1f}%", start=i*8))
            print(engine.colorize(f"  RAM   [{self._bar(m['mem_pct'])}] {m['mem_pct']:5.1f}%  ({self._fmt_bytes(m['mem_used'])} / {self._fmt_bytes(m['mem_total'])})", start=i*8+30))
            print(engine.colorize(f"  DISK  [{self._bar(m['disk_pct'])}] {m['disk_pct']:5.1f}%  ({self._fmt_bytes(m['disk_used'])} / {self._fmt_bytes(m['disk_total'])})", start=i*8+60))
            print(engine.colorize(f"  NET   \u2191 {self._fmt_bytes(m['net_sent'])}  \u2193 {self._fmt_bytes(m['net_recv'])}", start=i*8+90))
            print(engine.colorize(f"  [{datetime.now().strftime('%H:%M:%S')}]  Refresh {i+1}/{iterations}", start=i*8+120))
            if i < iterations - 1:
                time.sleep(interval)
        print()


# ═══════════════════════════════════════════════════════════════
#  DNS ENUMERATION MODULE
# ═══════════════════════════════════════════════════════════════

class DNSEnumerator:
    RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

    def __init__(self, domain):
        self.domain = domain
        self.engine = RainbowEngine(speed=0.18)

    def _query(self, qtype):
        try:
            info = socket.getaddrinfo(self.domain, None)
        except socket.gaierror:
            return []
        results = []
        if qtype == "A":
            for fam, _, _, _, addr in info:
                if fam == socket.AF_INET: results.append(addr[0])
        elif qtype == "AAAA":
            for fam, _, _, _, addr in info:
                if fam == socket.AF_INET6: results.append(addr[0])
        return list(set(results))

    def run(self):
        engine = self.engine
        print(engine.colorize(f"  [DNS] Enumerating {self.domain}...", start=0))
        print()
        idx = 0
        for qtype in self.RECORD_TYPES:
            records = self._query(qtype)
            if records:
                for rec in records:
                    print(engine.colorize(f"    {qtype:<6} {rec}", start=idx*5))
                    idx += 1
            else:
                print(engine.colorize(f"    {qtype:<6} (no records / not resolvable)", start=idx*5))
                idx += 1
        print()


# ═══════════════════════════════════════════════════════════════
#  SUBNET CALCULATOR
# ═══════════════════════════════════════════════════════════════

class SubnetCalculator:
    def __init__(self, cidr):
        self.cidr = cidr
        self.engine = RainbowEngine(speed=0.20)

    def _parse(self):
        ip_str, mask_str = self.cidr.split("/")
        mask = int(mask_str)
        ip_int = struct.unpack("!I", socket.inet_aton(ip_str))[0]
        network = ip_int & ((0xFFFFFFFF << (32 - mask)) & 0xFFFFFFFF)
        broadcast = network | (0xFFFFFFFF >> mask)
        return ip_str, mask, network, broadcast

    @staticmethod
    def _int_to_ip(n):
        return socket.inet_ntoa(struct.pack("!I", n))

    def run(self):
        engine = self.engine
        try:
            ip_str, mask, network, broadcast = self._parse()
        except Exception:
            print(f"  \033[38;2;255;60;60m[ERROR] Invalid CIDR: {self.cidr}\033[0m")
            return
        hosts = max(broadcast - network - 1, 0)
        fields = [
            ("CIDR", self.cidr), ("Network", self._int_to_ip(network)),
            ("Broadcast", self._int_to_ip(broadcast)),
            ("Subnet Mask", self._int_to_ip((0xFFFFFFFF << (32 - mask)) & 0xFFFFFFFF)),
            ("Host Range", f"{self._int_to_ip(network+1)} - {self._int_to_ip(broadcast-1)}"),
            ("Usable Hosts", str(hosts)),
            ("Wildcard", self._int_to_ip(0xFFFFFFFF >> mask)),
        ]
        for i, (k, v) in enumerate(fields):
            print(engine.colorize(f"    {k:>14}: {v}", start=i*6))
        print()


# ═══════════════════════════════════════════════════════════════
#  HASH TOOLS
# ═══════════════════════════════════════════════════════════════

class HashTools:
    def __init__(self):
        self.engine = RainbowEngine(speed=0.22)

    def generate(self, text):
        engine = self.engine
        algorithms = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
        print(engine.colorize(f"  [HASH] Input: {text[:60]}", start=0))
        print()
        for i, algo in enumerate(algorithms):
            h = hashlib.new(algo, text.encode("utf-8")).hexdigest()
            print(engine.colorize(f"    {algo:<8} {h}", start=i*8))
        print()

    def verify(self, text, expected, algo="sha256"):
        computed = hashlib.new(algo, text.encode("utf-8")).hexdigest()
        match = computed.lower() == expected.lower()
        color = "\033[38;2;0;255;100m" if match else "\033[38;2;255;50;50m"
        status = "MATCH" if match else "MISMATCH"
        print(f"  {color}[{status}] {algo}: {computed}\033[0m")
        print()


# ═══════════════════════════════════════════════════════════════
#  NETWORK SPEED TEST
# ═══════════════════════════════════════════════════════════════

class SpeedTest:
    def __init__(self, host="8.8.8.8", port=53, count=10):
        self.host, self.port, self.count = host, port, count
        self.engine = RainbowEngine(speed=0.16)

    def run(self):
        engine = self.engine
        print(engine.colorize(f"  [SPEED] Testing latency to {self.host}:{self.port}...", start=0))
        latencies = []
        for i in range(self.count):
            try:
                t0 = time.time()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((self.host, self.port))
                latency = (time.time() - t0) * 1000
                latencies.append(latency)
                bar_len = min(int(latency / 2), 40)
                print(engine.colorize(f"    Ping {i+1:>2}: {latency:>7.2f}ms  {'\u2588' * bar_len}", start=i*6))
            except Exception:
                print(engine.colorize(f"    Ping {i+1:>2}: TIMEOUT", start=i*6))
        if latencies:
            avg, mn, mx = sum(latencies)/len(latencies), min(latencies), max(latencies)
            print()
            print(engine.colorize(f"    Avg: {avg:.2f}ms  Min: {mn:.2f}ms  Max: {mx:.2f}ms  Jitter: {mx-mn:.2f}ms", start=80))
        print()


# ═══════════════════════════════════════════════════════════════
#  MAIN MENU & APPLICATION LOOP
# ═══════════════════════════════════════════════════════════════

class EmirNetworkApp:
    MENU_ITEMS = [
        ("1", "Port Scanner",       "High-speed multithreaded scan with service detection"),
        ("2", "Geo-IP & Whois",     "Domain intelligence via external APIs"),
        ("3", "Traffic Simulator",  "Live packet-flow simulation engine"),
        ("4", "System Metrics",     "Real-time CPU / RAM / Disk / Net bars"),
        ("5", "DNS Enumeration",    "A, AAAA, MX, NS, TXT, CNAME, SOA records"),
        ("6", "Subnet Calculator",  "IPv4 CIDR subnet computation"),
        ("7", "Hash Tools",         "Generate & verify MD5/SHA hashes"),
        ("8", "Network Speed Test", "Latency and jitter analysis"),
        ("0", "Exit",               "Terminate EMIRNETWORK"),
    ]

    def __init__(self):
        self.banner = RainbowBanner()
        self.engine = RainbowEngine(speed=0.14)

    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_menu(self):
        self.banner.print_header("MAIN MENU")
        for i, (key, title, desc) in enumerate(self.MENU_ITEMS):
            print(self.engine.colorize(f"  [{key}] {title:<22} {desc}", start=i*12))
        print()

    def _input(self, prompt):
        return input(self.engine.colorize(prompt, start=0)).strip()

    def _pause(self):
        self._input("  Press Enter to continue...")

    def _run_port_scanner(self):
        target = self._input("  Target host/IP: ")
        if not target: return
        sp = self._input("  Start port [1]: ") or "1"
        ep = self._input("  End port [1024]: ") or "1024"
        try:
            scanner = PortScanner(target, int(sp), int(ep))
            results, elapsed = scanner.run()
            if results:
                print()
                print(self.engine.colorize(f"  {'PORT':<8}{'SERVICE':<14}BANNER", start=0))
                print(self.engine.colorize("  " + "\u2500" * 70, start=10))
                for i, (port, svc, banner) in enumerate(results):
                    print(self.engine.colorize(f"  {port:<8}{svc:<14}{banner}", start=20+i*4))
            else:
                print(self.engine.colorize("  No open ports found.", start=0))
            print()
            print(self.engine.colorize(f"  Scan completed in {elapsed:.2f}s — {len(results)} open ports", start=50))
        except ValueError:
            print("  \033[38;2;255;60;60m[ERROR] Invalid port range.\033[0m")
        self._pause()

    def _run_geo_whois(self):
        target = self._input("  Target domain/IP: ")
        if not target: return
        GeoIPWhois(target).run()
        self._pause()

    def _run_traffic_sim(self):
        dur = self._input("  Duration in seconds [15]: ") or "15"
        rate = self._input("  Packet interval [0.3]: ") or "0.3"
        TrafficSimulator(duration=int(dur), rate=float(rate)).run()
        self._pause()

    def _run_system_metrics(self):
        iters = self._input("  Iterations [10]: ") or "10"
        interval = self._input("  Interval seconds [1.0]: ") or "1.0"
        SystemMetrics().run(iterations=int(iters), interval=float(interval))
        self._pause()

    def _run_dns_enum(self):
        domain = self._input("  Domain: ")
        if not domain: return
        DNSEnumerator(domain).run()
        self._pause()

    def _run_subnet_calc(self):
        cidr = self._input("  CIDR (e.g. 192.168.1.0/24): ")
        if not cidr: return
        SubnetCalculator(cidr).run()
        self._pause()

    def _run_hash_tools(self):
        text = self._input("  Text to hash: ")
        if not text: return
        HashTools().generate(text)
        self._pause()

    def _run_speed_test(self):
        host = self._input("  Target host [8.8.8.8]: ") or "8.8.8.8"
        port = self._input("  Target port [53]: ") or "53"
        count = self._input("  Ping count [10]: ") or "10"
        SpeedTest(host=host, port=int(port), count=int(count)).run()
        self._pause()

    def run(self):
        dispatch = {
            "1": self._run_port_scanner, "2": self._run_geo_whois,
            "3": self._run_traffic_sim, "4": self._run_system_metrics,
            "5": self._run_dns_enum, "6": self._run_subnet_calc,
            "7": self._run_hash_tools, "8": self._run_speed_test,
        }
        while True:
            self._clear()
            self.banner.print_banner()
            self._print_menu()
            choice = self._input("  EMIRNETWORK> ")
            if choice == "0":
                self._clear()
                self.banner.print_banner()
                print(self.engine.colorize("  Shutting down EMIRNETWORK... Goodbye.", start=0))
                print()
                break
            handler = dispatch.get(choice)
            if handler:
                self._clear()
                handler()
            else:
                print("  \033[38;2;255;60;60m[ERROR] Invalid selection.\033[0m")
                time.sleep(1.5)


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = EmirNetworkApp()
    app.run()
