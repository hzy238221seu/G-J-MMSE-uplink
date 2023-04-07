# VSCODE Launch Enhancer

## Structure
`.vscode`<br/>
`|----configure-into.py`<br/>
`|----launch.json`<br/>
`|----prototype-configurations.json`<br/>
`|----READ.md`<br/>
`|----show-configurations.py`<br/>
`|----show-pids.py`<br/>

## Usage
1. `launch.json` is generated automatically extracted from a `*-configurations.json` file, so you do not need to modify it directly. 
2. `prototype-configurations.json` is an example to organize your configurations. 
3. `*.py` scripts running by command line is not recommanded and use VSCODE `Run and Debug` in which all configurations have been done not explicitly. 
4. `.show-*` (except `.show-pids`) in VSCODE `Run and Debug` represent the actions to show a configuration files. 
5. `.configure-*` in VSCODE `Run and Debug` represent the actions to configure a `*-configurations.json` into `launch.json`. 
6. `.show-pids` demonstrates the running PID recorded in files with the suffix `.log` in current project directory with such files record PID in the format of `pid: {PID}`. 