#!/usr/bin/env python
import json
import urllib
import os


def ip2addr(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip
    ip_info = json.loads(urllib.urlopen(url).read())
    country_id = ip_info['data']['country_id']
#    addr = '%s[%s%s%s]'%(ip,ip_info['data']['country_id'],ip_info['data']['region'],ip_info['data']['city'])
    return country_id
def main():
    ip_list = open("/tmp/ip.list","r+b").readlines()
    for i in ip_list:
        ip = i.rstrip("\n")
        country_id = ip2addr(ip)
        if country_id == "US":
            os.system("iptables -A INPUT -s %s -j DROP" % ip )
            print country_id, ip
    

#a=ip2addr("8.8.4.4")
main()

