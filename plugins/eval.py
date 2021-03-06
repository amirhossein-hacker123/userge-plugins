import os
import asyncio
import subprocess
from userge import userge, Message, Config
import time
import sys
import random
import string

S_LOG = userge.getCLogger(__name__)

def randomName(length=10):
    return ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase+string.digits) for i in range(length)])

@userge.on_cmd("eval", about={
    'header': "Execute python code",
    'description': "Execute python code and get output",
    'usage': "{tr}eval [code]",
    'examples': "**For Text:** `{tr}eval print('test')`"})
async def eval(message: Message):
    if message.input_str and message.input_str.strip():
        code = message.input_str
        
        error_data = ""
        
        filename = randomName()
        filename_out = filename + "_out.txt"
        filename_err = filename + "_err.txt"

        original_output = sys.stdout
        original_error = sys.stderr

        sys.stdout = open(filename_out,'w')
        sys.stderr = open(filename_err,'w')

        a = time.time()
        try:
            exec(code)
        except Exception as ex:
            exception_type , exception_object , exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno

            error_data = f'{exception_type} {line_number} {str(ex)}'

        elapsed = round(time.time() - a,3)

        sys.stdout = original_output
        sys.stderr = original_error

        msg = f'''
**• Ⲥⲟⲙⲙⲁⲛⲇ:**
`{code}`

**• Ⲉʀʀⲟʀ:**
`{error_data}`

**• Ⲟυⲧⲣυⲧ:**
`{open(filename_out,'r').read()}`

**Ⲧⲓⲙⲉ Ⲉⳑⲁⲣⲋⲉⲇ**: `{elapsed}s`'''
        await message.edit(msg)
    else:
        await message.edit('Invalid usage')

