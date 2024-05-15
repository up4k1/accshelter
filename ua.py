from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Пример использования
if __name__ == "__main__":
    user_agent = get_random_user_agent()
    print(f"Случайный User Agent: {user_agent}")
