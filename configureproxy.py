def load_proxy_list(file_path):
    """ Загружает список прокси из файла """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        logging.error(f"Proxy file not found: {file_path}")
        return []

def parse_proxy(proxy_string):
    """ Разбирает строку прокси и возвращает тип прокси, IP, порт, имя пользователя и пароль (если есть) """
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
            # Default to http if not specified
            proxy_type = 'http'
            ip_port = address

        # Разбиваем адрес на IP и порт, предполагая, что порт всегда последний после последнего двоеточия
        *ip_parts, port = ip_port.split(':')
        ip = ':'.join(ip_parts)  # Это позволит корректно обработать IPv6

        return proxy_type, ip, int(port), user, password
    except Exception as e:
        logging.error(f"Error parsing proxy {proxy_string}: {str(e)}")
        return None, None, None, None, None


def configure_proxy(options, proxy_type, ip, port, username=None, password=None):
    """ Настраивает прокси для Selenium Options """
    if proxy_type == 'socks5':
        options.add_argument(f'--proxy-server=socks5://{ip}:{port}')
    elif proxy_type == 'socks4':
        options.add_argument(f'--proxy-server=socks4://{ip}:{port}')
    elif proxy_type == 'http':
        options.add_argument(f'--proxy-server={ip}:{port}')

    if username and password:
        options.add_argument(f'--proxy-auth={username}:{password}')
