import json
import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

group_info_dict = {"past": 0}


class groupBot:
    
    def __init__(self, group_id=False, group_join=False, auto_moderate=False, auto_role=False, sales_tracker=False, webhook=False, clothing_requirements=False):
        self.clothing_requirements = clothing_requirements
        self.group_join = group_join
        self.auto_moderate = auto_moderate
        self.auto_role = auto_role
        self.sales_tracker = sales_tracker
        self.webhook = webhook
        self.group_id = group_id
        
        if group_id == False:
            raise Exception("group_id not defined")
        
        else:
            group_info_dict["group_id"] = group_id
            group_info_dict["group_join"] = group_join
            group_info_dict["auto_moderate"] = auto_moderate
            group_info_dict["auto_role"] = auto_role
            group_info_dict["sales_tracker"] = sales_tracker
            
        
            
            
            
    def main_program(self):
        self.join()
        
    def join(self):
        
        while True:
            past = group_info_dict["past"]
            error = False  
            group_info = requests.get(f"https://groups.roblox.com/v1/groups/{group_info_dict['group_id']}").json()
            try:
                now = group_info["memberCount"]
                
            except:
                error = True
                
                
            if error == False:
                
                if past == 0:
                    past = now
                    
                if now > past:
                    users_joined = now - past
                    past = now
                    
                    members = requests.get(f"https://groups.roblox.com/v1/groups/{group_info_dict['group_id']}/users?sortOrder=Desc&limit=100").json()
                    for i in range(users_joined):
                        print(f"User {members['data'][i]['user']['username']} has just joined the group")
                        
                        if self.webhook != False:
                            
                            webhookk = DiscordWebhook(url=self.webhook)
                            embed = DiscordEmbed(title='New Member Joined', description=f"{members['data'][i]['user']['username']} has joined the group", color='03b2f8')
                            webhookk.add_embed(embed)
                            response = webhookk.execute()
                            
                        
            group_info_dict["past"] = past      
            error = False
            run other programs
            if self.auto_moderate == True:
                self.moderator(self.group_id, group_info_dict["cookie"], group_info_dict["token"])
                
            if self.auto_role == True:
                self.role()
            time.sleep(100)
            
    def auth(self, cookie):
        #logs in as the cookie supplied
        try:
            headers = {"Cookie": F".ROBLOSECURITY={cookie}"}
            XCSRF = requests.post("https://auth.roblox.com/v2/login", headers=headers).headers["x-csrf-token"]
        except Exception as Error:
            print(Error)
            return False
            
        
        auth_header = {"Cookie": F".ROBLOSECURITY={cookie}", "X-CSRF-TOKEN": XCSRF}
        try:
            user_id = requests.get("https://users.roblox.com/v1/users/authenticated", headers=auth_header).json()["id"]
            return XCSRF, user_id
        
        except:
            return False
        
        
    def moderator(self, group_id, cookie, token):


        wall_messages = []
        wall_id = []
        wall_user = []
        wall_data = requests.get("https://groups.roblox.com/v2/groups/" + str(group_id) + "/wall/posts?sortOrder=Desc&limit=100").json()

        for i in wall_data["data"]:
            wall_messages.append(i["body"])
            wall_id.append(i["id"])
            try:
                wall_user.append(i["poster"]["user"]["username"])
                
            except:
                wall_user.append("Roblox")
                


        messages = wall_messages, wall_id, wall_user


        count = 0
        for i in messages[0]:
            if "http" in i or "roblox.com" in i:
                delete_req = requests.delete("https://groups.roblox.com/v1/groups/" + str(group_id) + "/wall/posts/" + str(messages[1][count]), headers = {"Cookie": F".ROBLOSECURITY={cookie}", "X-CSRF-TOKEN": token}).json()
                webhookk = DiscordWebhook(url=self.webhook)
                embed = DiscordEmbed(title=f'{messages[2][count]} message was deleted', description=i, color='03b2f8')
                webhookk.add_embed(embed)
                response = webhookk.execute()

            else:
                return False

            count = int(count) + 1
            
            
    def role(self):
        users = []
        
        try:
            if self.auto_role == True:
                
                
                #get all rolesW
                roles_array = []
                roles_info = requests.get(f"https://groups.roblox.com/v1/groups/{self.group_id}/roles").json()
                print(roles_info)
                for i in roles_info["roles"]:
                    #print(f"Role Name: {i['name']}, Role Id: {i['id']}")
                    roles_array.append(str(i["id"]))
                    
                
                
                #get requirements
                if self.clothing_requirements == False:
                    raise Exception("clothing_requirements not defined in groupBot arguments")
                
                
                
                
                
                else:
                    
                    
                    dict_keys = self.clothing_requirements.keys()
                    for i in dict_keys:
                        try:
                            roles_array.index(i)
                            
                            
                        except:
                            raise Exception(f"Role ID: {i}, Not Found")
                
                #loop around members
                
                data = requests.get(f"https://groups.roblox.com/v1/groups/{self.group_id}/users?sortOrder=Asc&limit=100").json()
                for i in data["data"]:
                    users.append(i["user"]["userId"])
                try:
                    next_key = data["nextPageCursor"]
                    
                except:
                    next_key = False
                    
                if next_key == False:
                    return False
                
                else:
                    while next_key != False:
                        data = requests.get(f"https://groups.roblox.com/v1/groups/{self.group_id}/users?sortOrder=Asc&limit=100&cursor={next_key}").json()
                        
                        try:
                            for i in data["Data"]:
                                users.append(i["user"]["userId"])
                            try:
                                next_key = data["nextPageCursor"]
                                
                            except:
                                next_key = False
                                
                        except:
                            next_key = False
                            
                            
                
                            
                #get groups clothing here
                error = 0
                success = 0
                for user in users:
                    clothing_purchased = 0
                    try:
                        clothing = requests.get(f"https://www.roblox.com/users/inventory/list-json?assetTypeId=11&cursor=&itemsPerPage=100&pageNumber=1&sortOrder=Desc&userId={user}").json()
                        for x in clothing["Data"]["Items"]:
                            if x["Creator"]["Id"] == self.group_id:
                                clothing_purchased += 1
                                
                                
                        dict_keys = self.clothing_requirements.keys()
                        for i in dict_keys:
                            if self.clothing_requirements[i] <= clothing_purchased:
                                #print(i)
                                myobj = {"roleId": int(i)}
                                role_req = requests.patch("https://groups.roblox.com/v1/groups/" + str(self.group_id) + "/users/" + str(user), data=myobj, headers = {"Cookie": F".ROBLOSECURITY={group_info_dict['cookie']}", "X-CSRF-TOKEN": group_info_dict["token"]}).json()
                                try:
                                    role_req["errors"]
                                    error += 1

                                except:
                                    success += 1
                                
                                
                                    
                                
                            
                            
                    except:
                        pass
                    
                    
                print(f"Finished checking users inventorys, error: {error}, success: {success}")
                
        except KeyboardInterrupt:
            sys.exit()
                    
                        
                    
                    
            
        
            
    def run(self, cookie=None):
            
        if cookie == None:
            self.main_program()
            
            
        else:
            auth_info = self.auth(cookie)
            
            if auth_info == False:
                raise Exception("cookie is not valid")
            else:
                group_info_dict["cookie"] = cookie
                group_info_dict["id"] = auth_info[1]
                group_info_dict["token"] = auth_info[0]
                print("Bot Online")
                self.main_program()
            
            
#56309025
#bot = groupBot(auto_moderate=True, group_id=9301245, auto_role=True, clothing_requirements={"56309025": 0}, webhook="https://discord.com/api/webhooks/937457274560069672/clwq892s0tpMaNnFKWcPMjBSwS6m_-q7qqDnSxUo7_b9cfwCtYZuZ1HVghNuXFq0SSOV")
#bot.run(cookie="_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_00C9B687B4435D3FB89EE8FBCAEEED9C25726C7EA04350E8A382A6D62F5AA54B4623CC8CB4A47DFAA5D69D3EC55265C2E1338E75E0B64E1AF84AF92B9435BD80CCBE6AEF4BF940008AE3619A5A081AB9D32E0504FCEFF14B8250F6FC5ADDFFB59AE6716164694784FF4FDBF1E0758BED53EBCB9944B92B87A48EB7898A07217E4974307CF287CD158B8A6008D00F82BCE289DFEB6127944BCB8482F433DF6552B71DA0EF73454F88BC09A78C046B3D9D587CA880F708B22182804500E47565C8F05268CF6D01B0D3745C35794C276E75790FB0C2B334D13E7DACA5D15006F8F84E795959F1A0786270551EF26C497A155D132A7FCFFAC0929A53C9E19784B12D6AC055E587522209A650C0CC43525A3EBEB976A99EBEF69E7DB952C85ABE6FEE51AC8BFF95A3826AEE56CF14235915EBBD76B27E3AF9922ECF8E156B000E41195DBB08851645E5F3235E36B70FC54CD6E90DD083")
            


