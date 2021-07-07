import os
import asyncio
import requests
from userge import userge, Message, Config

S_LOG = userge.getCLogger(__name__)

@userge.on_cmd("banall", about={
    'header': "Ban all",
    'description': "Ban all users",
    'usage': "{tr}moveusers [group1]",
    'examples': "**For Text:** `{tr}banall test1`"})
async def searchdb(message: Message):
	client = message.client
	gg = message.input_str.split(' ')

	g1 = gg[0]
	if gg[1] == '1':
		g1 = int(gg[0])

	await message.edit('Getting members list...')
	ll = await client.get_chat_members(g1,limit=999999)
	await message.edit('Ban all')
	for i in ll:
		try:
			await client.kick_chat_member(g1,i.user.id)
		except:
			pass
	await message.edit('Completed')
