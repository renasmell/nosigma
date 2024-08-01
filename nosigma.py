import time
import requests
from colorama import Fore

auth = ""
userid = ""
channelid = ""
filter_term = "sigma"

color = {
    'success': Fore.GREEN,
    'choice': Fore.YELLOW,
    'default': Fore.WHITE,
    'input': Fore.LIGHTBLUE_EX,
    'item': Fore.LIGHTYELLOW_EX
}
                                                                       
def printTitle():
    print(f"""      
    {Fore.RED} /$$   /$$  /$$$$$$  {Fore.BLACK} /$$$$$$  /$$$$$$  /$$$$$$  /$$      /$$  /$$$$$$ 
    {Fore.RED}| $$$ | $$ /$$__  $${Fore.BLACK} /$$__  $$|_  $$_/ /$$__  $$| $$$    /$$$ /$$__  $$
    {Fore.RED}| $$$$| $$| $$  \\ $${Fore.BLACK}| $$  \\__/  | $$  | $$  \\__/| $$$$  /$$$$| $$  \\ $$
    {Fore.RED}| $$ $$ $$| $$  | $${Fore.BLACK}|  $$$$$$   | $$  | $$ /$$$$| $$ $$/$$ $$| $$$$$$$$
    {Fore.RED}| $$  $$$$| $$  | $${Fore.BLACK} \\____  $$  | $$  | $$|_  $$| $$  $$$| $$| $$__  $$
    {Fore.RED}| $$\\  $$$| $$  | $${Fore.BLACK} /$$  \\ $$  | $$  | $$  \\ $$| $$\\  $ | $$| $$  | $$
    {Fore.RED}| $$ \\  $$|  $$$$$$/{Fore.BLACK}|  $$$$$$/ /$$$$$$|  $$$$$$/| $$ \\/  | $$| $$  | $$
    {Fore.RED}|__/  \\__/ \\______/ {Fore.BLACK} \\______/ |______/ \\______/ |__/     |__/|__/  |__/

     > by renascent{Fore.WHITE}
    """)

def getMessages(auth=auth, channelid=channelid, userid=userid, filter_term=filter_term):
    headers = {'Content-Type': 'application/json', 'authorization': auth }
    messages = []
    offset = 0
    while len(messages) < 50 or offset != 200:
        r = requests.get(f"https://discord.com/api/v9/channels/{channelid}/messages/search?author_id={userid}&content={filter_term}&offset={offset}", headers=headers)

        tempm = []
        for e in r.json()["messages"]:
            msg = e[0]["content"]
            author_id = e[0]["author"]["id"]
            msg_id = e[0]["id"]
            type = e[0]["type"]
            if (author_id == userid): 
                # flag messages found
                tempm.append(0)
                # filter out deletables
                if type != 4:
                    messages.append({'message': msg, 'msg_id': msg_id, 'type': type })
        if len(tempm) == 25:
            offset += 25
            time.sleep(.1)
            pass
        else:
            break
        
    return messages

def doMainChoices():
    global channelid
    global auth 
    global userid
    global filter_term

    def printChoices(): return print(f"""
    (---------------------------------------------------------------------------)
    > Menu
     {color["default"]}1. {color["choice"]}start                                #
     {color["default"]}2. {color["choice"]}set channel                          | {color['item']}{channelid}
     {color["default"]}3. {color["choice"]}set auth                             : {color['item']}{auth}
     {color["default"]}4. {color["choice"]}set user_id                          | {color['item']}<@{userid}>
     {color["default"]}5. {color["choice"]}set custom word                      : {color['item']}{filter_term}
     {color["default"]}0. {color["choice"]}exit{color["default"]}
    """)
    def getInp(txt=": > "): return input(color["input"] + txt + color["default"])
    printTitle()
    while True:
        printChoices()

        choice = getInp("choice : > ")
        try: choice = int(choice)
        except: raise Exception("must be an int")

        if choice == 1:
            # start
            doScript()
            break
        elif choice == 2:
            print("enter new channel id")
            channelid = getInp() 
            print(f"{color["success"]}!set channel id to {color['item'] + channelid}{color["default"]}")
        elif choice == 3:
            print("enter new authentification")
            auth = getInp()
            print(f"{color["success"]}!set auth to {color['item'] + auth}{color["default"]}")
        elif choice == 4:
            print("enter new user id")
            userid = getInp()
            print(f"{color["success"]}!set user id to {color['item'] + userid}{color["default"]}")
        elif choice == 5:
            print("enter new custom word")
            filter_term = getInp()
            print(f"{color["success"]}!set custom word to {color['item'] + filter_term}{color["default"]}")
        elif choice == 0:
            print("exiting...")
            break
        else:
            pass

def doScript():
    global channelid 
    global auth
    global userid
    global filter_term
    msgs = getMessages(channelid=channelid,auth=auth,userid=userid,filter_term=filter_term)

    if len(msgs) <= 0:
        print(f"no messages found containing {filter_term}")
        return doMainChoices()
    print(f"found {len(msgs)} occurences of {filter_term}")

    while True:
        print(f"""
        {color["default"]}0.{color['choice']} return to main menu.     
        {color["default"]}1.{color['choice']} begin removal.
        """)

        try: a = int(input(f"{color['input']}choice : > "))
        except: raise Exception("must be an int")

        if (a == 1):
            # do deletions
            rate_limit = 0
            for m in msgs:
                r = requests.delete(f"https://discord.com/api/v9/channels/{channelid}/messages/{m["msg_id"]}", headers={'Content-Type': 'application/json', 'authorization': auth })
                if r.status_code > 400:
                    rate_limit += .1
                elif rate_limit > 0:
                    rate_limit -= .1

                time.sleep(.5 + rate_limit)
                print(f"{Fore.RED}- {m["message"]} {r.status_code}")
            print(f"{Fore.LIGHTGREEN_EX}> finished.")
            input(f"{color['default']}press any key to return to main menu.")
            return doMainChoices()
        elif (a == 0):
            return doMainChoices() 
        else:
            pass
    
doMainChoices()