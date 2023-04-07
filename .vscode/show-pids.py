import os
import re
from prettytable import PrettyTable


show_dict = {}
for log in filter(lambda x: x.endswith('.log'), os.listdir('.')):
    with open(log, encoding='utf-8') as f:
        txt = f.read().split('\n')
    for t in txt[:10] if len(txt) >= 10 else txt[0:]:
        s = re.search('pid: [0-9]+', t)
        if s:
            pid = int(s.group().split(' ')[1])
            show_dict[log] = pid
            break
table = PrettyTable(['log file', 'pid'])
table.add_rows(list(show_dict.items()))
table.sortby = 'pid'
print(table)
