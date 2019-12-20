# coding:utf-8 


import os
import requests
import json

access_token = ''
api_url = 'https://api.zoomeye.org/user/login'

def login():
    #user = input('input username:')
    #passwd = input('input password:')
    user = '377781971@qq.com'
    passwd = 'lhr961105'
    data = {
        'username' : user,
        'password' : passwd
    }
    data_encoded = json.dumps(data)
    try:
        r = requests.post(url = api_url, data = data_encoded)
        res = json.loads(r.text)
        access_token = res['access_token']
        return access_token
    except Exception:
        print('username or password is wrong')
        exit()


def stdin(access_token):
    header = {
        'Authorization' : 'JWT ' + access_token
    }
    
    query = input('search for(solr):')
    c="北京，天津，上海，重庆，河北，山西，辽宁，吉林，黑龙江，江苏，浙江，安徽，福建，江西，山东，河南，湖北，湖南，广东，海南，四川，贵州，云南，陕西，甘肃，青海，台湾，内蒙古，广西，西藏，宁夏，新疆，香港，澳门"
    a="".join(c)
    provs=a.split('，')
    for prov in provs:
        q = query
        q = q + " country:\"CN\" subdivisions:" + prov
        for p in range(1,21):
            url = 'https://api.zoomeye.org/host/search?query=%s&facet=app,os&page=%d' %(q, p)
            
            #print(q)
            search(url, header)





def search(url, header):
    print(url)
    try:
        re = requests.get(url, headers = header)
        res = json.loads(re.text)
        print(res)
        #print(res['matches'])
            
        with open("targets.txt",'w+') as f:
            for nes in res['matches']:
                ip = str(nes['ip'])
                portinfo = nes['portinfo']
                port = str(portinfo['port'])
                fin = ip + ":" + port
                print(fin)
                f.write(fin + '\n')
                
    except Exception as e:
        print(e)
        #exit()
    

def main():
    access_token = login()
    stdin(access_token)


if __name__ == "__main__":
    main()





'''
响应示例

{ "matches": [ {
    "geoinfo": {
        "asn": 45261,
        "city": {
            "names": {
                "en": "Brisbane",
                "zh-CN": "\u5e03\u91cc\u65af\u73ed"
            }
        },
        "continent": {
            "code": "OC",
            "names": {
                "en": "Oceania",
                "zh-CN": "\u5927\u6d0b\u6d32"
            }
        },
        "country": {
            "code": "AU",
            "names": {
                "en": "Australia",
                "zh-CN": "\u6fb3\u5927\u5229\u4e9a"
            }
        },
        "location": {
            "lat": -27.471,
            "lon": 153.0243
        }
    },
    "ip": "192.168.1.1",
    "portinfo": {
        "app": "",
        "banner": "+OK Hello there.\r\n-ERR Invalid command.\r\n\n",
        "device": "",
        "extrainfo": "",
        "hostname": "",
        "os": "",
        "port": 110,
        "service": "",
        "version": ""
    },
    "timestamp": "2016-03-09T16:14:04"
    }, ... ...],
   "facets": {
   },
    "total": 28731397
}
'''