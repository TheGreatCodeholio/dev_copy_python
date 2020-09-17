#!/usr/bin/env python3

# Import Python 3 modules.
import os
import time
import logging


# Import Our Classes
from lib.text_color import Colors
from lib.user_input_handler import UserInput
from lib.sshkey_handler import ssh_key
from lib.backup_source_database import backup_source_database
from lib.import_source_database import import_source_database
from lib.rsync_source_files import rsync_source_files
from lib.m1_config import m1_config
from lib.m1_finalize import m1_finalize
from lib.m2_config import m2_config
from lib.m2_finalize import m2_finalize


def main():
    # Get User Input
    user_input = UserInput()
    # Put User Input in to a Dictionary
    settings_dict = user_input.settings_dict
    print(Colors.OKGREEN + str(settings_dict) + Colors.ENDC)
    # Check for SSH Key, Generate is there isn't one, add path to the settings dict
    settings_dict["sou_ssh_privkey_path"] = ssh_key(settings_dict["sou_ssh_user"])
    # Read Public Key
    pub_key = os.popen("cat /srv/.ssh/" + settings_dict["sou_ssh_user"] + ".pub").read()
    print(Colors.WARNING + "Add SSH Key to Source Stratus User: " + Colors.OKGREEN + settings_dict["sou_ssh_user"] + Colors.ENDC)
    print(Colors.OKBLUE + pub_key + Colors.ENDC)
    input("Press Enter to continue...")
    tar_ip = os.popen("curl http://ipcheck.com/").read()
    print(Colors.WARNING + "Add SSH User " + Colors.OKGREEN + settings_dict["sou_ssh_user"] + Colors.WARNING + " to source whitelist and add IP address: " + Colors.OKGREEN + tar_ip + Colors.ENDC)
    input("Press Enter to continue...")
    # Backup Source Database
    print(Colors.OKGREEN + "Starting Source Database Backup" + Colors.ENDC)
    time.sleep(1.5)
    backup_source_database(settings_dict)
    # RSYNC Database from Source to Target and Import
    print(Colors.OKGREEN + "Starting Import Database From Source" + Colors.ENDC)
    time.sleep(1.5)
    import_source_database(settings_dict)
    # RSYNC Files from Source to Target
    print(Colors.OKGREEN + "Starting RSYNC Files From Source" + Colors.ENDC)
    time.sleep(1.5)
    rsync_source_files(settings_dict)
    # Check Magento Version We are Working With and Finish Up.
    if settings_dict["m_version"] == 1:
        # Create Config M1
        print(Colors.OKGREEN + "Doing Dev Copy Configuration for Magento 1" + Colors.ENDC)
        time.sleep(1.5)
        m1_config(settings_dict)
        m1_finalize(settings_dict)
        print(Colors.OKGREEN + "Copy Successful! Please make sure the Docroot is set to: " + settings_dict["sou_public_html"])
    else:
        # Create Config M2
        print(Colors.OKGREEN + "Doing Dev Copy Configuration for Magento 2" + Colors.ENDC)
        time.sleep(1.5)
        m2_config(settings_dict)
        m2_finalize(settings_dict)
        print(Colors.OKGREEN + "Copy Successful! Please make sure the Docroot is set to: " + settings_dict["sou_public_html"])

if __name__ == '__main__':
    main()
    logging.basicConfig(level=logging.WARN)
