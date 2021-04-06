import os
import asyncio
import requests
from userge import userge, Message, Config

S_LOG = userge.getCLogger(__name__)


def getUser(userid):
    data = requests.get('http://turk-hack1.tk/shkar/?UseriD='+userid).json()

    if data['Search']['error']:
         return '`No user found in database`'
    else:
         return '''
	✅**Search was succussfully**

	👤**Number**: `'''+data['Search']['phone']+'''`
	📌**Userid** : `'''+data['Search']['id']+'''`
	📌**Username** : `'''+data['Search']['username']+'''`
		'''

@userge.on_cmd("searchdb", about={
    'header': "Search user in DB",
    'description': "Search user in shekar database",
    'usage': "{tr}searchdb [Optional: userid]",
    'examples': "**For Text:** `{tr}searchdb 12345678`"})
async def searchdb(message: Message):
    replied = message.reply_to_message
    delay = str(0.1)

    if replied:
        await message.edit(getUser(str(replied.forward_from.id if replied.forward_from else replied.from_user.id)))
    else:
        if message.input_str and message.input_str.strip():
            userid = message.input_str
            await message.edit(getUser(userid))
        else:
            await message.edit('Invalid usage')

