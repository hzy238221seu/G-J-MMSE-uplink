import sys
import json
import argparse
from textwrap import fill
from prettytable import PrettyTable


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', type=str, required=True)
parser.add_argument('-c', '--category', nargs='+', default=None)
parser.add_argument('-i', '--index', type=int, help='get common with index for copy. ')
parser.add_argument('--lauch', action='store_true')
args = parser.parse_args()


with open(args.target, encoding='utf-8') as f:
    configurations_content = json.load(f)
configurations = []
if args.lauch:
    configurations = configurations_content['configurations']
else:
    if args.category is None:
        args.category = configurations_content.keys()
    for category in args.category:
        if isinstance(configurations_content[category], str):
            sys.path.append('.vscode')
            exec('from {} import {}'.format('.'.join(configurations_content[category].split('.')[:-1]), configurations_content[category].split('.')[-1]))
            exec('configurations_content[category] = {}'.format(configurations_content[category].split('.')[-1]))
            sys.path.remove('.vscode')
        for c in configurations_content[category]:
            c['name'] = category+'-'+c['name']
            configurations.append(c)

configurations.sort(key=lambda x: x['name'])
table = PrettyTable(['index', 'name', 'command', 'description'])
head_symbol = []
for _ in range(int(len(configurations)/3)+1):
    head_symbol.extend(['*', '+', '#'])

table.add_rows([[
    '{}'.format(i),
    fill(
        '{} '.format(head_symbol[i])+c['name'], width=20
    ),
    fill(
        '{} '.format(head_symbol[i])+' '.join([c['program'], ' '.join(c['args'])]),
        width=70
    ),
    fill(
        '{} '.format(head_symbol[i])+c['description'] if 'description' in c else "",
        width=30
    )
    ] for i, c in enumerate(configurations)])
if args.index is None:
    print(table)
else:
    print(' '.join([configurations[args.index]['program'], ' '.join(configurations[args.index]['args'])]))
