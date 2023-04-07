import os
import sys
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', type=str, required=True)
args = parser.parse_args()

with open(args.target, encoding='utf-8') as f:
    configurations = json.load(f)

launch = {'version': '0.2.0', 'configurations': []}
jsons = filter(lambda x: x.endswith('-configurations.json'), os.listdir('.vscode'))
launch['configurations'].append({
    "name": ".show-launch",
    "type": "python",
    "request": "launch",
    "program": ".vscode/show-configurations.py", 
    "console": "integratedTerminal",
    "justMyCode": True,
    "args": [
        "-t",
        ".vscode/launch.json",
        "--lauch"
    ]
})
for j in jsons:
    launch['configurations'].append({
        "name": ".configure-{}".format('-'.join(j.split('-')[:-1])),
        "type": "python",
        "request": "launch",
        "program": ".vscode/configure-into.py", 
        "console": "integratedTerminal",
        "justMyCode": True,
        "args": [
            "-t",
            os.path.join('.vscode', j)
        ]
    })
    launch['configurations'].append({
        "name": ".show-{}".format('-'.join(j.split('-')[:-1])),
        "type": "python",
        "request": "launch",
        "program": ".vscode/show-configurations.py", 
        "console": "integratedTerminal",
        "justMyCode": True,
        "args": [
            "-t",
            os.path.join('.vscode', j)
        ]
    })

for category in configurations:
    if isinstance(configurations[category], str):
        sys.path.append('.vscode')
        exec('from {} import {}'.format('.'.join(configurations[category].split('.')[:-1]), configurations[category].split('.')[-1]))
        exec('configurations[category] = {}'.format(configurations[category].split('.')[-1]))
        sys.path.remove('.vscode')
    for configuration in configurations[category]:
        configuration['name'] = category+'-'+configuration['name']
        launch['configurations'].append(configuration)

launch['configurations'].append(
    {
        "name": ".show-pids",
        "type": "python",
        "request": "launch",
        "program": ".vscode/show-pids.py", 
        "console": "integratedTerminal",
        "justMyCode": True,
    }
)

with open('.vscode/launch.json', 'w', encoding='utf-8') as f:
    json.dump(launch, f, indent=4)
