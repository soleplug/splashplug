from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import sys

fn = sys.argv[1]

proxy = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
    

driver = webdriver.Chrome(r"/Users/hasan/Downloads/chromedriver")
    
x = ""
driver.get('http://www.adidas.com/yeezy')
cookies = driver.get_cookies()
for cookie in cookies:

    if(cookie['name'] == 'RT'):
        s = list(cookie['value'])
        s[0] = "'"
        s[-1] = "'"
        x = x + (cookie['name'] + '=' + ''.join(s) + '; ') 
    else:
        x = x + (cookie['name'] + '=' + cookie['value'] + '; ') 
 
driver.quit()
x = x[:-2]
f= open(fn,"w")
f.write("""#!/bin/bash
args=("$@")
if [[ ${args[1]} == *"proxy"* ]]; then
    while true; do
        response=$(curl -x ${args[2]} -c ${args[0]} -s -k -i --compressed "http://www.adidas.com/us/apps/yeezy/" -H "Host: www.adidas.com" -H "Connection: keep-alive" -H "Cache-Control: max-age=0" -H "Upgrade-Insecure-Requests: 1" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: en-US,en;q=0.8" -H "Cookie: """ + x + """")
        if [[ $response == *"YEEZY"* ]]; then
            echo -n "."
        fi
    done
else
    while true; do
        response=$(curl -c ${args[0]} -s -k -i --compressed "http://www.adidas.com/us/apps/yeezy/" -H "Host: www.adidas.com" -H "Connection: keep-alive" -H "Cache-Control: max-age=0" -H "Upgrade-Insecure-Requests: 1" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: en-US,en;q=0.8" -H "Cookie: """ + x + """")
        if [[ $response == *"YEEZY"* ]]; then
            echo -n "."
        fi
    done
fi


""")
f.close()

"""while True:
    try:
        with open('cook', 'r') as fin:
            print(fin.read(), end = "")
    except:
        continue"""

    
