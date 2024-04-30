import tls_client, json, random, base64, time, os
from datetime import datetime

class General:
    def Clear_Screen():
        os.system("cls") if os.name == "nt" else os.system("clear")

    def Title(args=None):
        os.system("title Member Scraper ^| jwe0") if args == None else os.system("title Member Scraper ^| jwe0 ^| {}".format(args))

    def Menu():
        print("""


 __  __                _                 ____                                 
|  \/  | ___ _ __ ___ | |__   ___ _ __  / ___|  ___ _ __ __ _ _ __   ___ _ __ 
| |\/| |/ _ \ '_ ` _ \| '_ \ / _ \ '__| \___ \ / __| '__/ _` | '_ \ / _ \ '__|
| |  | |  __/ | | | | | |_) |  __/ |     ___) | (__| | | (_| | |_) |  __/ |   
|_|  |_|\___|_| |_| |_|_.__/ \___|_|    |____/ \___|_|  \__,_| .__/ \___|_|   
                                                             |_|              


""")



class Spoofers:
    def __init__(self, token) -> None:
        self.token = token
        self.session = tls_client.Session()

    def Cookies(self):
        response = self.session.get("https://canary.discord.com/api/v9/experiments")
        dcfduid = response.cookies.get("__dcfduid")
        sdcfduid = response.cookies.get("__sdcfduid")
        cfruid = response.cookies.get("__cfruid")

        return dcfduid, sdcfduid, cfruid



    def Xsuper(self, agent):
        os = random.choice(["Windows", "Mac OS X", "Linux", "iOS", "Android"])
        browser = random.choice(["Chrome", "Firefox", "Safari", "Edge", "Opera"])


        xsuper = {
            "os": os,
            "browser": browser,
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": agent,
            "browser_version": "116.0",
            "os_version": "10",
            "referrer": "https://e-z.bio/",
            "referring_domain": "e-z.bio",
            "referrer_current": "https://discord.com/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": 288460,
            "client_event_source": "null",
            "design_id": 0
        }

        super = json.dumps(xsuper)
        return base64.b64encode(super.encode()).decode()

    def User_Agent(self):
        return random.choice([agent for agent in open("Assets/Agents.txt").read().splitlines()])

    def Headers(self):
        agent = self.User_Agent()
        xsuper = self.Xsuper(agent)
        dcfduid, sdcfduid, cfruid = self.Cookies()



        headers = {
            "Host": "discord.com",
            "User-Agent": agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": self.token,
            "X-Super-Properties": xsuper,
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Europe/London",
            "X-Debug-Options": "bugReporterEnabled",
            "DNT": "1",
            "Alt-Used": "discord.com",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/1134536127928352859/1134536440173310006",
            "Cookie": f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; __cfruid={cfruid}; locale=en-US",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }

        return headers




class Scrape:
    def __init__(self, gid, token) -> None:
        self.guild_id = gid
        self.token = token
        self.headers = Spoofers(self.token).Headers()
        self.session = tls_client.Session()
        self.channel_ids = []
        self.members = {}


    def Channels(self):
        General.Title("Scraping {}".format(self.guild_id))
        url = "https://discord.com/api/v9/guilds/{}/channels".format(self.guild_id)
        response = self.session.get(url, headers=self.headers)

        for channel in response.json():
            self.channel_ids.append(channel['id'])

    
    def Messages(self):
        url = "https://discord.com/api/v9/channels/{}/messages?limit=100"

        channel_progress = 0
        message_progress = 0

        for channel in self.channel_ids:
            channel_progress += 1
            curr = f"[{str(channel_progress)}/{str(len(self.channel_ids))}]"
            print(f"[{str(channel_progress)}/{str(len(self.channel_ids))}]", end='\r')
            response = self.session.get(url.format(channel), headers=self.headers)

            for message in response.json():
                message_progress += 1
                print(f"{curr} - {str(message_progress)}/{len(response.json())}", end='\r')
                
                self.members[message['author']['id']] = message['author']['username']
            message_progress = 0

            time.sleep(1)
        print("Scraped server. Check Scrapes/{}.json for members".format(str(self.guild_id)))

        self.Dump()

    def Dump(self):
        with open(f"Scrapes/{str(self.guild_id)}.json", 'w') as f:
            json.dump(self.members, f, indent=4)



            
class Spam:
    def __init__(self, channel, guild, loops, maxmem) -> None:
        self.channel = channel
        self.guild = guild
        self.loops = loops
        self.maxmem = maxmem
        self.token = json.load(open("Assets/config.json")).get('Token')
        self.spoof = Spoofers(self.token)
        self.session = tls_client.Session()
        self.members = []

    def Get_Members(self):
        if os.path.exists("Scrapes/{}.json".format(self.guild)):
            with open("Scrapes/{}.json".format(self.guild)) as m:
                mems = json.load(m)

                for mem in mems:
                    self.members.append(mem)

    def Send_Message(self, message):
        url = "https://discord.com/api/v9/channels/{}/messages".format(self.channel)
        headers = self.spoof.Headers()

        data = {'content' : message}

        response = self.session.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}]\t{str(response.status_code)}\tSuccesfull")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}]\t{str(response.status_code)}\tFailed")


    def Start(self):
        for x in range(self.loops):
            message = "" 
            used = [] 

            for i in range(len(self.members)):
                if i not in used:
                    message += f"<@{self.members[i]}> "
                    used.append(i)

                    if len(used) == self.maxmem or i == len(self.members) - 1:
                        self.Send_Message(message)
                        message = ""
                        used = []




class Main:
    def __init__(self) -> None:
        self.token = ""

    def Load_Token(self):
        with open("Assets/config.json") as config:
            config = json.load(config)
            self.token = config['Token']






    def Main(self):
        General.Clear_Screen()
        General.Title()
        General.Menu()
        server = input("Server ID: ")
        print("1. Scrape\t2. Spam")
        selection = input("> ")
        match selection:
            case "1":
                s = Scrape(server, self.token)
                s.Channels()
                s.Messages()
            case "2":
                channel = input("Channel ID: ")
                loops = input("Loops: ")
                mp = input("Membes per: ")
                print()
                s = Spam(channel, server, int(loops), int(mp))
                s.Get_Members()
                s.Start()


    
if __name__ == "__main__":
    main = Main()
    main.Load_Token()
    main.Main()