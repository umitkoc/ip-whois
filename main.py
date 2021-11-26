from json import loads
from os import system
from sys import exit
import sys

import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
from whois import whois


class Main():
    def __init__(self) -> None:
        system("clear")
        page = """
          ______  ______    ______    ______     ______    ______    
         /\  == \/\  __ \  /\  == \  /\  ___\   /\  ___\  /\  == \   
         \ \  _-/\ \  __ \ \ \  __<  \ \___  \  \ \  __\  \ \  __<   
          \ \_\   \ \_\ \_\ \ \_\ \_\ \ \/\___\  \ \_____\ \ \_\ \_\ 
           \/_/    \/_/\/_/  \/_/ /_/  \/\____/   \/_____/  \/_/ /_/ 
        """
        print(page)
        input("start press key")
        self.array = []
        self.domainName = []
        self.name = 0
        self.step = 0
        self.filename=""
        self.readexcel()

    def readexcel(self):
        self.data = pd.DataFrame(pd.read_excel(self.filename, index_col=0)).sort_values(by=['dest_ip'], ascending=False)
        pd.set_option('display.max_rows', self.data.shape[0]+1)
        self.start()

    def start(self):
        for ip in self.data['dest_ip']:
            self.terminal(ip)
        self.read()

    def read(self):
        # self.data.insert(0, 'whois', self.array)
        system("clear")
        print(self.array)
        print("the end")

    def terminal(self, ip):
        try:
            if self.name != ip:
                data = whois(ip)
                if data['domain_name'] == None:
                    if data['emails'] == None:
                        print(f"not email: {data}")
                        exit(0)
                    else:
                        self.domainName = data['emails'][0]
                else:
                    self.domainName = data['domain_name']
        except:
            self.web_whatIs(ip)
            pass
        self.write(ip)

    def web_whatIs(self, ip):
        jsondata = loads(
            get(f"https://rdap.arin.net/registry/ip/{ip}").text)
        try:
            ## nameserver control
            data = jsondata['entities'][0]['vcardArray'][1][1][-1]
            if data != None:
                self.domainName = data
                self.write(ip)

        except:
            ##email control
            data = jsondata['entities'][-1]['vcardArray'][-1][-1][-1]
            self.domainName = data
            self.write(ip)
            pass

    def write(self, ip):
        self.array.append(self.domainName)
        self.name = ip
        self.step += 1
        print(f"step:{self.step}\n {ip}:{self.domainName}")


if __name__ == '__main__':
    main = Main()
