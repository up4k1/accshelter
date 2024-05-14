import logging

def load_proxy_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        logging.error(f"Proxy file not found: {file_path}")
        return []

def parse_proxy(proxy_string):
    try:
        if '@' in proxy_string:
            credentials, address = proxy_string.split('@')
            user, password = credentials.split(':')
        else:
            address = proxy_string
            user, password = None, None

        if address.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            proxy_type = address.split('://')[0]
            ip_port = address.split('://')[1]
        else:
            proxy_type = 'http'
            ip_port = address

        *ip_parts, port = ip_port.split(':')
        ip = ':'.join(ip_parts)

        return proxy_type, ip, int(port), user, password
    except Exception as e:
        logging.error(f"Error parsing proxy {proxy_string}: {str(e)}")
        return None, None, None, None, None

def configure_proxy(options, proxy_type, ip, port, username=None, password=None):
    options.set_preference("network.proxy.type", 1)
    if proxy_type == 'socks5':
        options.set_preference("network.proxy.socks", ip)
        options.set_preference("network.proxy.socks_port", port)
        options.set_preference("network.proxy.socks_version", 5)
        options.set_preference("network.proxy.socks_remote_dns", True)
    elif proxy_type == 'socks4':
        options.set_preference("network.proxy.socks", ip)
        options.set_preference("network.proxy.socks_port", port)
        options.set_preference("network.proxy.socks_version", 4)
    elif proxy_type == 'http':
        options.set_preference("network.proxy.http", ip)
        options.set_preference("network.proxy.http_port", port)
        options.set_preference("network.proxy.ssl", ip)
        options.set_preference("network.proxy.ssl_port", port)

    if username and password:
        options.set_preference("network.proxy.username", username)
        options.set_preference("network.proxy.password", password)
