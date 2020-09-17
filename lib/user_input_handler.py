import os
from lib.text_color import Colors
import re
import json
from datetime import date
import subprocess

class UserInput:
    def __init__(self):
        self.settings_dict = {}
        self.today = date.today()
        self.settings_dict["date"] = self.today.strftime("%d%B%Y")
        self.get_uuid()

    def get_uuid(self):
        tar_uuid = input(Colors.OKGREEN + "Target Instance UUID: " + Colors.ENDC)
        if len(tar_uuid) != 16:
            print(Colors.FAIL + "UUID must be exactly 16 Characters" + Colors.ENDC)
            self.get_uuid()
            return
        self.settings_dict["tar_uuid"] = tar_uuid
        # os.popen("cd instance_configs && wget --user=magemojo --ask-password -r -nH --cut-dirs=2 --no-parent --reject='index.html*' http://icarey.net/instance_configs")
        self.check_for_config()

    def check_for_config(self):
        if os.path.exists("instance_configs/" + self.settings_dict["tar_uuid"] + ".json"):
            print(Colors.OKGREEN + "Existing Config Found!" + Colors.ENDC)
            config_load = input(Colors.OKGREEN + "Would you like to load existing config? (y/n): " + Colors.ENDC)
            if config_load.lower() == "y" or config_load.lower() == "yes":
                print(Colors.OKGREEN + "Loading Existing Config..." + Colors.ENDC)
                with open("instance_configs/" + self.settings_dict["tar_uuid"] + ".json", 'r') as config_json:
                    self.settings_dict = json.load(config_json)
                    config_json.close()
            elif config_load.lower() == "n" or config_load.lower() == "no":
                print(Colors.WARNING + "Not Loading Existing Config..." + Colors.ENDC)
                self.get_mage_version()
            else:
                print(Colors.FAIL + "Answer with the following, Yes/Y or No/N" + Colors.ENDC)
                self.check_for_config()
                return
        else:
            print(Colors.FAIL + "Existing Config Not Found!" + Colors.ENDC)
            self.get_mage_version()

    def get_mage_version(self):
        m_version = input(Colors.OKGREEN + "Magento Version: " + Colors.ENDC)
        try:
            v_check = int(m_version)
            if v_check not in [1, 2]:
                raise ValueError
            else:
                self.settings_dict["m_version"] = v_check
                self.get_target_mysql_cred()
        except ValueError:
            print(Colors.FAIL + "Not a valid version. Either version 1 or 2." + Colors.ENDC)
            self.get_mage_version()

    def get_target_mysql_cred(self):
        os.system('/usr/share/stratus/cli database.config > cred.log 2>&1')
        self.settings_dict["tar_mysql_user"] = \
            os.popen("cat cred.log | grep Username | awk '{print $3}' | cut -c3- | rev | cut -c4- | rev").read().split(
                '\n')[0]
        self.settings_dict["tar_mysql_database"] = \
            os.popen("cat cred.log | grep Username | awk '{print $7}' | cut -c3- | rev | cut -c4- | rev").read().split(
                '\n')[0]
        self.settings_dict["tar_mysql_password"] = \
            os.popen("cat cred.log | grep Username | awk '{print $14}' | cut -c3- | rev | cut -c4- | rev").read().split(
                '\n')[0]
        os.system('rm cred.log')
        self.get_target_base()

    def get_target_base(self):
        child = subprocess.Popen("mysql -h mysql -u " + self.settings_dict["tar_mysql_user"] + " -p'" + self.settings_dict["tar_mysql_password"] + "' " + self.settings_dict["tar_mysql_database"] + " -e 'select value from core_config_data where path like \"web/%secure/base_url\" AND scope=\"default\" LIMIT 1'", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        print(rc)
        if rc == 1:
            base_url = input(Colors.OKGREEN + "Target Base URL: " + Colors.ENDC)
            if not base_url.endswith('/'):
                print("Base URL must end with a /.")
                self.get_target_base()
                return
            else:
                self.settings_dict["tar_base_url"] = base_url
        else:
            self.settings_dict["tar_base_url"] = streamdata.decode('UTF-8').split('value')[1].replace('\n', '')
            print(streamdata.decode('UTF-8').split('value')[1].replace('\n', ''))
        self.get_source_ssh_host()

    def get_source_ssh_host(self):
        sou_ssh_host = input(Colors.OKGREEN + "SSH Host IP: " + Colors.ENDC)
        try:
            ip_valid = [0 <= int(x) < 256 for x in
                        re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', sou_ssh_host).group(0))].count(True) == 4
            if not ip_valid:
                raise ValueError
            else:
                self.settings_dict["sou_ssh_host"] = sou_ssh_host
                self.get_source_ssh_port()
        except ValueError:
            print(Colors.FAIL + "Not a Valid IPv4 Address." + Colors.ENDC)
            self.get_source_ssh_host()
            return

    def get_source_ssh_port(self):
        sou_ssh_port = input(Colors.OKGREEN + "SSH Port: " + Colors.ENDC)
        self.settings_dict["sou_ssh_port"] = sou_ssh_port
        self.get_source_ssh_user()

    def get_source_ssh_user(self):
        sou_ssh_user = input(Colors.OKGREEN + "SSH User: " + Colors.ENDC)
        self.settings_dict["sou_ssh_user"] = sou_ssh_user
        self.get_source_public_html()

    def get_source_public_html(self):
        sou_public_html = input(Colors.OKGREEN + "Remote public_html path: " + Colors.ENDC)
        if sou_public_html.endswith('/'):
            print(Colors.FAIL + "Path should not end with a /. Example /srv/public_html" + Colors.ENDC)
            self.get_source_public_html()
            return
        else:
            self.settings_dict["sou_public_html"] = sou_public_html
            self.save_json_config()

    def save_json_config(self):
        print(Colors.OKGREEN + "Saving Config....." + Colors.ENDC)
        print(self.settings_dict)
        with open("instance_configs/" + self.settings_dict["tar_uuid"] + ".json", 'w') as outfile:
            json.dump(self.settings_dict, outfile, indent=4)
            outfile.close()
        # os.popen("rsync -Pav -e 'ssh -p 22' instance_configs/" + self.settings_dict["tar_uuid"] + ".json magemojo@play.icarey.net:~/")