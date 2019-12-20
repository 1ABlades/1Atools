#!/usr/bin/env python3
import requests
import re
import sys


rules = [
    r"(href|src).?=.?\\?\"(.*?)\"",
    r"\"(http:\/\/.*?)\""
    r"action.?=.?\"(.*?)\""
    # "([a-zA-z]+://[^\s]*)\""
]

# ignore = [
#     ".css",
#     "javascript:void(0)"
# ]


def stdcookie(cookie):
    cookies={}
    cookie=cookie.split(';')
    
    for c in cookie:
        c=c.strip().split('=')
        cookies[c[0]]=c[1]
    return cookies


def geturls(url,cookie):
    if cookie != 0:
        r=requests.get(url,cookies=cookie)
        #print(cookie)
    else:
        r=requests.get(url)
    res=r.content
    # ree=re.compile("(href|src)=\"(.*?)\"")
    links = set()
    for rule in rules:
        urls=re.findall(rule,res.decode('utf-8'))
        
        for url in urls:
            if len(url)==2:
                url = url[1]
            links.add(url)
    count=0
    for link in links:
        links=link.strip()
        # for ig in ignore:
        #     if ig in link:
        #         break
        #     else:
        #         print(link)
        #         count=count+1
        #         break
        print(links)
        count=count+1
    print(count)

if __name__ == "__main__":
    url=sys.argv[1]
    cookie = 0
    if len(sys.argv) > 2:
        cookie=sys.argv[2]
        cookie=stdcookie(cookie)
        geturls(url,cookie)
    else:
        geturls(url,cookie)
