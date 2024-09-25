import requests
from fake_useragent import UserAgent
from urllib.parse import quote
import random

# 定義API的URL
api_url = 'https://airdrop-api.gomble.io/walletChecker'

# 生成隨機的User-Agent
ua = UserAgent()
random_user_agent = ua.random

# 從檔案中讀取代理伺服器列表
with open('proxy.txt', 'r') as f:
    proxies_list = [line.strip() for line in f.readlines()]

# 從檔案中讀取錢包地址列表
with open('wallets.txt', 'r') as f:
    wallet_addresses = [line.strip() for line in f.readlines()]

# 遍歷每個錢包地址
for wallet_address in wallet_addresses:
    # 隨機選擇一個代理
    proxy_line = random.choice(proxies_list)
    proxy_parts = proxy_line.split(':')
    
    if len(proxy_parts) == 5:
        proxy_address = proxy_parts[0]
        proxy_port = proxy_parts[1]
        proxy_user = proxy_parts[2]
        proxy_pass = proxy_parts[3]
        proxy_type = proxy_parts[4]
        proxy_url = f"{proxy_type}://{proxy_user}:{proxy_pass}@{proxy_address}:{proxy_port}"
    elif len(proxy_parts) == 3:
        proxy_address = proxy_parts[0]
        proxy_port = proxy_parts[1]
        proxy_type = proxy_parts[2]
        proxy_url = f"{proxy_type}://{proxy_address}:{proxy_port}"
    else:
        continue  # 跳過格式不正確的代理

    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }

    # 定義請求頭
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': random_user_agent,
        # 其他必要的頭信息，如果有的話
    }

    # 定義請求數據
    data = {
        'walletAddress': wallet_address
    }

    # 發送POST請求到API
    response = requests.post(api_url, headers=headers, json=data, proxies=proxies)

    # 檢查響應狀態碼
    if response.status_code == 201:
        # 解析JSON響應
        response_data = response.json()
        wallet_info = response_data.get("walletInfo", [])
        if wallet_info:
            found_eligible = False
            for item in wallet_info:
                name = item['name']
                badge = item['badge']
                has_eligibility = item['hasEligibility']
                amount = item['amount']
                if amount > 0:
                    print(f"{name} / {badge} / {has_eligibility} / {amount}")
                    found_eligible = True
            if not found_eligible:
                print(f"{wallet_address} 不在白名單內")
        else:
            print(f"{wallet_address} 不在白名單內")
    else:
        print("請求失敗，狀態碼:", response.status_code)

    # 檢查並打印當前的IP地址
    ip_response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
    current_ip = ip_response.json().get('ip')
    print(f"當前IP地址: {current_ip}")