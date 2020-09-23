#!usr/bin/env python
#Password Locker
PASSWARDS = {'email':'lala123456',\
                    'blog':'jaja123456',\
                    'luggage': 'dw123456'  }

import sys,pyperclip

if len(sys.argv)<2:
    print('some errors')
    sys.exit()


account = sys.argv[1]  #First command line arg is the account name

if account in PASSWARDS:
    pyperclip.copy(PASSWARDS[account])
    print('Hooray! Password for '+account+' copied to clipboard.')
else:
    print('No account named'+account)