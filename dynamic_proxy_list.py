#!/bin/python3

"""
Get some Proxy IPs and put them in DB
Sheduled
"""

# TODO: python3 verification, hide passwd


import requests
import mysql.connector
import os
from getpass import getpass


PROTO = "https" #Hardcoded
ANON_CHOISE = ["anonymous", "elite", "transparent"]

def db_connect():
    mydb = mysql.connector.connect(
            host="localhost",
            user="python_daemon",
            database="proxy_list",
            passwd=getpass()
        )

    cur = mydb.cursor()

    return mydb, cur


def fetch_and_insert(mydb, cur, proxy, anon_type):


    for ip in proxy:
        IP, PORT= ip.split(":")

        sql_insert = 'INSERT INTO ip_list (IP, PORT, ANON) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE PORT=%s'
        sql_value = (IP, PORT, anon_type, PORT)

        try:
            cur.execute(sql_insert, sql_value)
            print("[+] OK INSERT", sql_insert, sql_value)
        except:
            print("[!] ERROR IN INSERT !", sql_insert, sql_value)


        mydb.commit()

    return cur, mydb



def get_proxyes(anon_type):

    ANON = anon_type
    URL = "https://www.proxy-list.download/api/v1/get?type="+PROTO+"&anon="+ANON+"&country=IT"

    req = requests.get(URL)
    if str(req.status_code) != "200":
        print("Url Error")

    result = req.text

    result = str(result)
    result = result.splitlines()

    return result

def main():

    mydb, cur = db_connect()
    #print("connesso")

    for anon_type in ANON_CHOISE:
        proxy_by_anon = get_proxyes(anon_type)
        #print(proxy_by_anon, anon_type)
        fetch_and_insert(mydb, cur, proxy_by_anon, anon_type)

    cur.close()
    mydb.close()



if __name__ == "__main__":

    if os.geteuid() != 0:
        exit("You need to use 'sudo'. Exiting.")

    main()
