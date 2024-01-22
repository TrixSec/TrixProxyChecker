import requests
from concurrent.futures import ThreadPoolExecutor
from pyfiglet import Figlet
from termcolor import colored

def check_proxy(proxy, target_url):
    try:
        response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return True
    except Exception as e:
        pass
    return False

def check_proxies_from_file(filename, target_url, num_threads):
    working_proxies = []

    try:
        with open(filename, 'r') as file:
            proxies = file.read().splitlines()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(check_proxy, proxy, target_url) for proxy in proxies]
            working_proxies = [proxy for proxy, is_working in zip(proxies, futures) if is_working]

    except Exception as e:
        print(f"Error: {e}")

    return working_proxies

def display_proxy_options():
    print("Proxy Types:")
    print("1 = HTTP")
    print("2 = HTTPS")
    print("3 = SOCKS4")
    print("4 = SOCKS5")
    print("00 = Back")

def print_banner():
    f = Figlet(font='block')
    banner_text = f.renderText('Trix Proxies Checker')
    colorful_banner = colored(banner_text, 'cyan')
    print(colorful_banner)

def main():
    print_banner()

    filename = input("Enter the filename containing proxies: ")
    target_url = input("Enter the target URL to check against: ")

    while True:
        display_proxy_options()
        choice = input("Enter the number for the type of proxy: ")

        if choice == "00":
            print("Going back.")
            return
        elif choice in {"1", "2", "3", "4"}:
            proxy_type = {'1': 'HTTP', '2': 'HTTPS', '3': 'SOCKS4', '4': 'SOCKS5'}[choice]
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        num_threads = int(input("Enter the number of threads for concurrent proxy checking: "))

        working_proxies = check_proxies_from_file(filename, target_url, num_threads)

        print("\nWorking Proxies:")
        for proxy in working_proxies:
            print(proxy)

        print(f"\nTotal Working Proxies: {len(working_proxies)}")
        print(f"Total Non-Working Proxies: {len(proxies) - len(working_proxies)}")

if __name__ == "__main__":
    main()
