#!/usr/bin/env python3
from subprocess import check_output
import json

config = check_output(['php', '-r', 'echo json_encode(include "config.php");'])
config = json.loads(config)

if "save" in config["session"]:
    print(config["session"]["save"])
print(config["queue"])