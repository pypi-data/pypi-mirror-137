python roblox api wrapper to help manage your roblox group AUTOMATICALLY

Example Input

import robloxapiwrapper

bot = robloxapiwrapper.groupBot(auto_moderate=True, group_id=9301245, auto_role=True, clothing_requirements={"role id": amount_of_clothing}, webhook="webhook")
bot.run(cookie="Enter Your Roblox Cookie Here")

Info:
    
- The account MUST be given max permissions eg: admin or this won't work and must be a VALID cookie!
- If it successfully runs you should see output the console which says "bot online"

- if auto_moderate is True it will delete any message in the group with a link in the message
- if auto_role is True it will automatically give a person a role depending on how many clothes they have purchased
- clothing_requirements must have the format {"role_id": amount, "1": 5} if a user has purchased 5 clothing in the group they will be given
role_id 1


