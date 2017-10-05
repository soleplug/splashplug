from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import sys
from selenium.webdriver.chrome.options import Options
import zipfile


fn = sys.argv[1]
try:
    proxy = sys.argv[2]
    ip = proxy.split(':')[0]
    port = proxy.split(':')[1]
    
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: """ + '"' + ip + '"' + """,
                port: parseInt(""" + port + """)
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "XXXXXXXXX",
                password: "XXXXXXXXX"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """


    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    co.add_argument("--start-maximized")
    co.add_extension(pluginfile)


    driver = webdriver.Chrome(r"/Users/hasan/Downloads/chromedriver",  chrome_options=co)

except:
    print("No proxy. If you did enter a proxy, there was an error starting chrome. Please quit...")
    # Change the path below to point to your chromedriver
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
        if [[ $response == *"sitekey"* ]]; then
            echo "Locate hmac in" $args[2]
            break
        fi
    done
else
    while true; do
        response=$(curl -c ${args[0]} -s -k -i --compressed "http://www.adidas.com/us/apps/yeezy/" -H "Host: www.adidas.com" -H "Connection: keep-alive" -H "Cache-Control: max-age=0" -H "Upgrade-Insecure-Requests: 1" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: en-US,en;q=0.8" -H "Cookie: """ + x + """")
        if [[ $response == *"sitekey"* ]]; then
            echo "Locate hmac in" $args[2]
            break
        fi
    done
fi


""")
f.close()

    
