import os
import asyncio
import requests
from userge import userge, Message, Config

S_LOG = userge.getCLogger(__name__)

@userge.on_cmd("moveusers", about={
    'header': "Move users",
    'description': "Move users from one group to another group",
    'usage': "{tr}moveusers [group1] [group2] [count]",
    'examples': "**For Text:** `{tr}moveusers test1 test2 100`"})
async def searchdb(message: Message):
    client = message.client
    gg = message.input_str.split(' ')
    
    g1 = gg[0]
    g2 = gg[1]
    count = int(gg[2])

    for i in client.get_chat_members(g1,limit=count):
        
        client.add_chat_members(g2,i.user.id)