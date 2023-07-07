import psutil
import csv
import pandas as pd
from datetime import datetime
from requests import get
import time
import os
# import speedtest-cli
import speedtest
import socket
import json
import apikey


output_file = os.path.join('/Users/Michael/Documents/Programmering/Python-projekt', 'out.csv')
internet_file = os.path.join('/Users/Michael/Documents/Programmering/Python-projekt', 'internet.csv')
startTime = time.time()
toMegaBit = 1000000


def geo_api_ip(ip):
    url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"
    querystring = {"ip":ip}
    headers = apikey.headers
    response = requests.request("GET", url, headers=headers, params=querystring)
    geo_api_response = json.loads(response.text)
    if(200==response.status_code):
        # country = geo_api_response['country']
        return geo_api_response['city']
    else:
        return None
def speed_measure():
    now = time.time()
    if(now > startTime + 3600*3):
            startTime = now
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("www.duckduckgo.com",80))
                localIP = (s.getsockname()[0])
                Ext_ip = get('https://api.ipify.org').text
                s.close()
                city = geo_api_ip(Ext_ip)
                h_name = socket.gethostname()
                IP_adress = socket.gethostbyname(h_name)
                s = speedtest.Speedtest()
                download = round((s.download()/toMegaBit),2)
                upload = round((s.upload()/toMegaBit),2)
                df = pd.DataFrame({'Download': [download],
                                    'Upload': [upload],
                                    'Latency': [s.results.ping],
                                    'IP_adress': [localIP],
                                    'Ext_IP': [Ext_ip],
                                    'City': [city],
                                    'Time': [date]})
                df.to_csv(internet_file, index=False, mode='a', header=False)
            except:
                df = pd.DataFrame({'Download': ['0']})


if __name__ == '__main__':
    while(True):
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        date = datetime.today().strftime("%Y-%m-%d %H:%M")
        df = pd.DataFrame({'Plugged': [plugged],
                           'Battery_percentage': [percent],
                           'Timestamp': [date]})
        df.to_csv(output_file, index=False, mode='a', header=False)
        time.sleep(120)
