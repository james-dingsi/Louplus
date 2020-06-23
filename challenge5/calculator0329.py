#!/usr/bin/env python3
import sys
import csv
import getopt
import time
from configparser import ConfigParser
from collections import namedtuple   

sb = ConfigParser()

class Args:
    '''参数处理类
    '''

    def __init__(self):
        self.args = sys.argv[1:]
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hc:o:d:C:',)
        except getopt.GetoptError:
            print(usage)
            sys.exit(1)

        for a, f in opts:
            if a == '-c':
                self.sb_config = f
            elif a == '-o':
                self.pl_file = f
            elif a == '-d':
                self.ud_file = f
            elif a == '-C':
                self.config_city = f.upper()
            else:
                print(usage)


    def city(self):
        return self.config_city

    def config_files(self):
        return self.sb_config

    def userdata(self):
        return self.ud_file

    def paylist(self):
        return self.pl_file


class Config:
    '''配置文件处理类
    '''

    def __init__(self, config_file_name):
        sb.read(readfiles.config_files(), encoding='utf-8')
        if readfiles.city() in sb.sections():

            sb_list = sb.items(readfiles.city())
        else:
            sb_list = sb.items('DEFAULT')

#        print(sb_list)

        for a, b in sb_list:
            shebao_config[a] = float(b)
 #       print(shebao_config)

    def sb_pay(self, tax_before): 
        self.tax_before = tax_before
        shebaorate = 0
        for a, b in shebao_config.items():
            if b < 1:
                shebaorate += b
        for x, y in tax_before.items():
            shebao_pay = y * shebaorate
            if y > shebao_config['jishul']:
                shebao_pay = shebao_config['jishuh'] * shebaorate
            if y < shebao_config['jishul']:
                shebao_pay = shebao_config['jishuh'] * shebaorate
            sb_pay_dict[x] = [tax_before.get(x), shebao_pay]
        return shebao_pay
    
 
class Output:
    '''导出数据类
    '''

    def personal_tax(self):   
        IncomeTax = namedtuple(
            'IncomeTax',
            ['Yingshui', 'Taxrate', 'Sunsuankc']
            )
        Qizheng = 5000
        tax_tuple = [
            IncomeTax(80000, 0.45, 15160),
            IncomeTax(55000, 0.35, 7160),
            IncomeTax(35000, 0.30, 4410),
            IncomeTax(25000, 0.23, 2660),
            IncomeTax(12000, 0.20, 1410),
            IncomeTax(3000, 0.1, 210),
            IncomeTax(0, 0.03, 0)
            ]
        for x, y in sb_pay_dict.items():
            Yingshui = y[0] - Qizheng - y[1]
            for item in tax_tuple:
                if Yingshui > item.Yingshui:
                    pers_tax = Yingshui * item.Taxrate
                    real_pay = y[0] - y[1] - pers_tax
                else:
                    pers_tax = 0
                    real_pay = y[0] - y[1]
                output_dict[x] = [int(y[0]), round(y[1], 2), 
                        round(pers_tax, 2), round(real_pay, 2)]


shebao_config = {}   
sb_pay_dict = {}  
output_dict = {}    
userdata_dict = {}    


class Userdata:
    '''用户数据处理类
    '''

    def __init__(self, userdata_files):
        with open(userdata_files) as ud_f:
            userdata = csv.reader(ud_f)
            for u in userdata:
                userdata_dict[u[0]] = float(u[1])


if __name__ == '__main__':
    usage = 'Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata'

    readfiles = Args()
    calculation = Config(readfiles.config_files())
    user = Userdata(readfiles.userdata())
    sb_cal = calculation.sb_pay(userdata_dict)
    output = Output()
    output.personal_tax()

    with open(readfiles.paylist(), 'w') as pl:
        csv.writer(pl).writerows(output_dict.items())
