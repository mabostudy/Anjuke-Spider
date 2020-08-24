import requests,re

ips1=[]
ip_list=[]
def get_ips():
    response=requests.get('http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip')
    ips=re.findall("\\d+\\.\\d+\\.\\d+\\.\\d*\\:\\d+",response.text,re.S)
    for ip in ips:
        try:
            proxies = {'https': "https://" +ip}  # 必须是字典
        except Exception as e:
            print(e)
        try:
            test_ip_response = requests.get('https://sh.fang.anjuke.com/',
                                            proxies=proxies)
            if test_ip_response.status_code == 200:
                ip_list.append(proxies)
        except Exception as e:
            print(e)
    print("可用的代理有:")
    print(ip_list)
    return ip_list
