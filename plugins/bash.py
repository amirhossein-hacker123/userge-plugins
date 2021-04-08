import os
import asyncio
import subprocess
from userge import userge, Message, Config
import time

S_LOG = userge.getCLogger(__name__)

@userge.on_cmd("bash", about={
    'header': "Execute bash command",
    'description': "Execute bash command and get output",
    'usage': "{tr}searchdb [command]",
    'examples': "**For Text:** `{tr}bash ls`"})
async def bash(message: Message):
    if message.input_str and message.input_str.strip():
        command = message.input_str
        
        await message.edit('`Executing command...`')
        
        a = time.time()
        result = subprocess.run(command.split(' '), capture_output=True, text=True)
        elapsed = round(time.time() - a,3)
        
        msg = f'''

**• Ⲥⲟⲙⲙⲁⲛⲇ:**
`{command}`

**• Ⲉʀʀⲟʀ:**
`{result.stderr}`

**• Ⲟυⲧⲣυⲧ:**
`{result.stdout}`

**Ⲧⲓⲙⲉ Ⲉⳑⲁⲣⲋⲉⲇ**: `{elapsed}s`'''
        await message.edit(msg)
    else:
        await message.edit('Invalid usage')

