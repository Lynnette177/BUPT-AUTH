import requests
import re
cookies = None
Account = ''
Password = ''
def extract_values(html_content):
    # 定义正则表达式模式
    # 使用正则表达式找到匹配项
    execution_value = re.search(r'<input\s+name="execution"\s+value="([^"]+)"', html_content)

    if execution_value:
        execution_value = execution_value.group(1)
        print(execution_value)
    else:
        print("WTF!!!!!!")
    return execution_value

def get_and_print(url):
    global cookies
    try:
        response = requests.get(url, allow_redirects=False)
        print("Initial URL:", response.url)
        while response.status_code == 302:  # 302状态码表示重定向
            redirected_url = response.headers['Location']
            print("Redirected to:", redirected_url)
            response = requests.get(redirected_url, allow_redirects=False)
        if response.status_code == 200:
            cookies = response.cookies
            print(cookies)
            return extract_values(response.text)
        else:
            print("Failed to retrieve content. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def get_login_cookies (username, password,exe):
    url = "https://auth.bupt.edu.cn/authserver/login"  # 替换为实际的登录URL
    data = {
        'username': username,
        'password': password,
        'submit': '登录',
        'type': 'username_password',
        'execution': exe,
        '_eventId': 'submit',
    }
    print(data)
    try:
        print(cookies)
        response = requests.post(url, data=data,allow_redirects=False,cookies=cookies)
        redirected_url = response.headers['Location']
        for cookie in response.cookies:
            print(cookie)
        print("重定向地址:", redirected_url)
        response = requests.post(redirected_url, data=data, allow_redirects=False, cookies=response.cookies)
        for cookie in response.cookies:
            print(cookie)
        return response.cookies
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def get_co_and_sa:
    url1 = "https://app.bupt.edu.cn/buptdf/wap/default/chong"
    exe = get_and_print(url1)
    return get_login_cookies(Account, Password,exe)
