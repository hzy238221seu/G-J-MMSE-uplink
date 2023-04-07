configs = [
    {
        "name": "prototype{}".format(i),
        "type": "python",
        "request": "launch",
        "program": "script.py",
        "console": "integratedTerminal",
        "justMyCode": True,
        "args": [
            "-h"
        ]
    } for i in range(3)
]