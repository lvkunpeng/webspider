# -*-coding: utf-8 -*-

import re

line = 'bobby123'
reg_str = '(bobby|boobby)123'
match_obj = re.match(reg_str,line)
if match_obj:
    print(match_obj.group(1))