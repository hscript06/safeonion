import subprocess
import os
import signal
import time


TOR_DIR = os.path.join(os.path.dirname(__file__), "tor-browser")
TOR_EXEC = os.path.join(TOR_DIR, "start-tor-browser.desktop")
tor_proc = None
privoxy_proc = None

def detect_distro():
    try:
        with open("/etc/os-release") as f:
            data = f.read().lower()
        if "debian" in data or "ubuntu" in data or "mint" in data or "pop" in data:
            return "debian"
        elif "arch" in data or "manjaro" in data or "endeavouros" in data:
            return "arch"
        elif "fedora" in data or "centos" in data or "rhel" in data or "rocky" in data:
            return "fedora"
        else:
            return "unknown"
    except:
        return "unknown"
DISTRO = detect_distro()

def check_services():
    print("🔍 Checking services...")
    if subprocess.call(["which", "tor"], stdout=subprocess.DEVNULL) != 0:
        print("❌ Tor is not installed")
        if DISTRO == "debian":
            print("📦 Installing Tor...")
            subprocess.run(["sudo","apt","install","tor"])
        elif DISTRO == "arch":
            print("📦 Installing Tor...")
            subprocess.run(["sudo","pacman","-S","tor"])
        elif DISTRO == "fedora":
            print("📦 Installing Tor...")
            subprocess.run(["sudo","dnf","install","tor"])
        else:
            print("📦 Install it with your package manager")
    else:
        print("✅ Tor installed")
    if subprocess.call(["which", "privoxy"], stdout=subprocess.DEVNULL) != 0:
        print("❌ Privoxy is not installed")
        if DISTRO == "debian":
            print("📦 Installing Privoxy...")
            subprocess.run(["sudo","apt","install","privoxy"])
        elif DISTRO == "arch":
            print("📦 Installing Privoxy...")
            subprocess.run(["sudo","pacman","-S","privoxy"])
        elif DISTRO == "fedora":
            print("📦 Installing Privoxy...")
            subprocess.run(["sudo","dnf","install","privoxy"])
        else:
            print("📦 Install it with your package manager")
    else:
        print("✅ Privoxy installed")

        config_path = "/etc/privoxy/config"
        try:
            with open(config_path, "r") as f:
                config_content = f.read()

            if "forward-socks5t / 127.0.0.1:9050 ." not in config_content:
                print("⚠ Proxy configuration not found. Adding...")
                with open(config_path, "a") as f:
                    f.write("\nforward-socks5t / 127.0.0.1:9050 .\n")
                print("✅ Configuration added successfully.")
            else:
                print("✅ Proxy configuration is correct.")
        except PermissionError:
            print(f"⚠ Could not access {config_path}. Run with permissions to check and modify.")

def kill_processes(name):
    try:
        subprocess.call(["pkill", "-f", name])
    except Exception as e:
        print(f"⚠ Could not kill {name}: {e}")
        print(f"⚠ but don't worry, this is normal, it's just a security measure")

def start_services():
    global tor_proc, privoxy_proc
    print("\n🚀 Starting services...")
    kill_processes("tor")
    kill_processes("privoxy")
    time.sleep(1)

    privoxy_proc = subprocess.Popen(["privoxy", "--no-daemon", "/etc/privoxy/config"])
    time.sleep(2)  
    tor_proc = subprocess.Popen(["tor"])
    time.sleep(5)

def launch_tor_browser1():
    print(f"🌐 Opening Tor Browser at: the hidden wiki")
    subprocess.Popen([TOR_EXEC, "--url", "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page"], cwd=TOR_DIR)

def launch_tor_browser2():
    print(f"🌐 Opening Tor Browser at: onion search")
    subprocess.Popen([TOR_EXEC, "--url", "http://oniondxjxs2mzjkbz7ldlflenh6huksestjsisc3usxht3wqgk6a62yd.onion"], cwd=TOR_DIR)

def stop_services():
    print("🛑 Stopping services...")
    if privoxy_proc:
        privoxy_proc.terminate()
    if tor_proc:
        tor_proc.terminate()
    print("✅ Services stopped")

def welcome():
    print(r""" 
    ######################################################
                    __                  _             
         ___  __ _ / _| ___  ___  _ __ (_) ___  _ __  
        / __|/ _` | |_ / _ \/ _ \| '_ \| |/ _ \| '_ \ 
        \__ \ (_| |  _|  __/ (_) | | | | | (_) | | | |
        |___/\__,_|_|  \___|\___/|_| |_|_|\___/|_| |_|
    
    ######################################################
    """)

def url_questions():
    while True:
        print("\nBefore starting, choose what you want to launch")
        print("1 - the hidden wiki (most common)")
        print("2 - onion search (onion search engine with possible unsafe pages)")
        start_choice = input("\n>>").strip()
        if start_choice == "1":
            print("😶‍🌫️ enjoy your privacy 😶‍🌫️")
            start_services()
            launch_tor_browser1()
            break
        elif start_choice == "2":
            print("😶‍🌫️ enjoy your privacy 😶‍🌫️")
            start_services()
            launch_tor_browser2()
            break
        else:
            print("❌ Invalid option, try again.")

def main():
    welcome()
    try:
        if DISTRO == "debian":
            print("⚪ Your distribution is: Debian/Ubuntu/Mint/Pop!_OS")
        elif DISTRO == "arch":
            print("⚪ Your distribution is: Arch/Manjaro/EndeavourOS")
        elif DISTRO == "fedora":
            print("⚪ Your distribution is: Fedora/CentOS/RHEL/Rocky")
        else:
            print("⚠ Your distribution was not found, the script may not work 100%")
        check_services()
        url_questions()
        input("\nPress ENTER to close everything...\n")
        
    finally:
        stop_services()

if __name__ == "__main__":
    main()