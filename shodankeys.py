#!/usr/bin/python2
# coding: utf-8
import shodan
from datetime import datetime
from colorama import Fore
import colorama
import sys

ctime = datetime.now()
time = str(ctime.month) + "_" + str(ctime.day) + "_" + str(ctime.hour) + "_" + str(ctime.minute) + "_" + str(ctime.second)
paid_results_file = open("./results/" + time + "-valid_paid.txt", "w+")
results_file = open("./results/" + time + "-valid_community.txt", "w+")

colorama.init()
def test(key):
    api = shodan.Shodan(key)
    try:
        info = api.info()
    except Exception:
        print Fore.RED + "[-] Key %s is invalid!" %(key)
        return False,False
    if info['plan'] == 'dev': #this seems to be how they are categorized
        print Fore.GREEN + "[+] Key " + key + " valid | Plan: Freelancer | Scan credits: " + str(info['scan_credits'])
        paid_results_file.write(key + " | Plan: Freelancer | Scan credits: " + str(info['scan_credits']) + "\n")
        return True,True
    elif info['plan'] == 'edu':
        print Fore.GREEN + "[+] Key " + key + " valid | Plan: Small Buisness | Scan credits: " + str(info['scan_credits'])
        paid_results_file.write(key + " | Plan: Small Buisness | Scan credits: " + str(info['scan_credits']) + "\n")
        return True,True
    elif info['plan'] == 'oss':
        print Fore.BLUE + "[~] Key " + key + " valid | Plan: Community"
        results_file.write(key + " | Plan: Community | Scan credits: " + str(info['scan_credits']) + "\n")
        return True,False


def main(args):
    if len(args) != 2:
        sys.exit("Shodan API Key List Checker (for testing githubbed keys)\nusage: %s keys-to-test.txt" %(args[0]))
    f = open(args[1], "r")
    keys = f.readlines()
    valid_keys = []
    paid_keys = []
    comm_keys = []
    for key in keys:
        key = key.strip()
        is_valid,is_paid = test(key=key)
        if is_valid == True:
            valid_keys.append(key)
            if is_paid == True:
                paid_keys.append(key)
            else:
                comm_keys.append(key)
        else:
            pass
    print(Fore.WHITE)
    print "\n\n[+] Acquired %d valid keys" %(len(valid_keys))
    print "[+] Acquired %d paid-keys" %(len(paid_keys))
    print "[+] Acquired %d community-keys" %(len(comm_keys))
    print "\n[+] Paid Keys..."
    for key in paid_keys:
        print key
    print "\n[+]Community Keys..."
    for key in comm_keys:
        print key


if __name__ == "__main__":
    main(args=sys.argv)
