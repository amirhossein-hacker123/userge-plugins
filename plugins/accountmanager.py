import os
import asyncio
import subprocess
from userge import userge, Message, Config
import time
import sys
import random
import string
import ftplib
from concurrent.futures import ThreadPoolExecutor,as_completed
from pyrogram import Client

S_LOG = userge.getCLogger(__name__)

def checkAccountsDir():
	if not os.path.exists("accounts"):
		os.mkdir('accounts')

def getFTP():
	return ftplib.FTP(os.environ['FTP_HOST'],user=os.environ['FTP_USER'],passwd=os.environ['FTP_PASS'])

@userge.on_cmd("fetchaccs", about={
	'header': "Fetch all telegram Accounts",
	'description': "Fetch all telegram Accounts",
	'usage': "{tr}fetchaccs",
	'examples': "**For Text:** `{tr}fetchaccs`"})
async def fetchaccs(message: Message):
	checkAccountsDir()

	ftp = getFTP()
	ftp.cwd('/htdocs/accounts')

	await message.edit('Start fetching accounts...')
	accounts = []
	for i in ftp.nlst():
		if i.endswith('.session'):
			ftp.retrbinary(f'RETR {i}',open('accounts/'+i,'wb').write)
			accounts.append(i)

	await message.edit('Accounts Fetched :\n'+'\n'.join(accounts))


@userge.on_cmd("delaccs", about={
	'header': "Delete all telegram Accounts",
	'description': "Delete all telegram Accounts",
	'usage': "{tr}delaccs",
	'examples': "**For Text:** `{tr}fetchaccs`"})
async def fetchaccs(message: Message):
	checkAccountsDir()

	await message.edit('Starting deleting accounts...')
	for i in os.scandir('accounts'):
		os.remove('accounts/'+i.name)

	await message.edit('All account sessions are removed successfully:)')

@userge.on_cmd("evalaccs", about={
	'header': "Run an code to all accounts",
	'description': "Run an code to all accounts",
	'usage': "{tr}evalaccs [threadsCount] [code]",
	'examples': "**For Text:** `{tr}evalaccs 50 app.block('username')`"})
async def evalaccs(message: Message):
	checkAccountsDir()

	arr = message.input_str.split(' ')

	threads = int(arr[0])
	code = ' '.join(arr[1:])

	def __code(acc):
		if acc.endswith('.session'):
			acc = acc.replace('.session','')

			app = Client('accounts/'+acc,
				api_id=7796848,
				api_hash="0bed1015bfde57a87ea96c4c940567da"
			)
			app.start()

			try:
				exec(code)
				return f'{acc} Completed'
			except Exception as ex:
				exception_type , exception_object , exception_traceback = sys.exc_info()
				line_number = exception_traceback.tb_lineno

				error_data = f'{acc} {exception_type} {line_number} {str(ex)}'

				app.stop()

				return error_data
			app.stop()

	with ThreadPoolExecutor(max_workers = threads) as executor:
		await message.edit('Start doing...')
		futures = {executor.submit(__code , acc.name): acc for acc in os.scandir('accounts')}

		data = ""
		exceptions = ""
		for future in as_completed(futures):
			try:
				data += str(future.result()) + "\n"
			except Exception as exc:
				exceptions += str(exc) + "\n"
		
		await message.edit(exceptions + "\n" + data)