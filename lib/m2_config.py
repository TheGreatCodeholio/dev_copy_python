import os
from datetime import datetime, date, time, timezone
from lib.text_color import Colors
import subprocess
import json


class m2_config:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict
        self.m2_config_json = {}
        self.init_config()

    def init_config(self):
        if not os.path.exists(self.settings_dict["sou_public_html"] + "/app/etc/env.php"):
            print(Colors.FAIL + "Magento 2 Configuration doesn't exist, exiting" + Colors.ENDC)
            exit(1)
        load_config = subprocess.check_output(["php", "-r", "echo json_encode(include '" + self.settings_dict["sou_public_html"] + "/app/etc/env.php');"])
        self.m2_config_json = json.loads(load_config)
        self.config_database()

    def config_database(self):
        print(Colors.OKGREEN + "Configuring Database." + Colors.ENDC)
        os.popen("php " + self.settings_dict["sou_public_html"] + "/bin/magento setup:config:set -n --db-host=mysql --db-name=" + self.settings_dict["tar_mysql_database"] + " --db-user=" + self.settings_dict["tar_mysql_user"] + " --db-password=" + self.settings_dict["tar_mysql_password"] + " --db-prefix=" + self.m2_config_json["db"]["table_prefix"]).read()
        self.config_downloadable_domains()

    def config_downloadable_domains(self):
        print(Colors.OKGREEN + "Configuring Downloadable Domains." + Colors.ENDC)
        os.popen("php " + self.settings_dict["sou_public_html"] + "/bin/magento downloadable:domains:add " + self.settings_dict["tar_base_url"].split('https://')[1].split('/')[0]).read()
        self.update_base_url()

    def update_base_url(self):
        print(Colors.OKGREEN + "Updating Base URL" + Colors.ENDC)
        os.popen("mysql -h mysql -u " + self.settings_dict["tar_mysql_user"] + " -p\"" + self.settings_dict["tar_mysql_password"] + "\" " + self.settings_dict["tar_mysql_database"] + " -e 'update " + self.m2_config_json["db"]["table_prefix"] + "core_config_data set value=\"" + self.settings_dict["tar_base_url"] + "\" where path like \"web/%secure/base_url\" AND scope=\"default\"'").read()
        self.update_cookie_domain()

    def update_cookie_domain(self):
        print(Colors.OKGREEN + "Updating Cookie Domain" + Colors.ENDC)
        os.popen("mysql -h mysql -u " + self.settings_dict["tar_mysql_user"] + " -p\"" + self.settings_dict["tar_mysql_password"] + "\" " + self.settings_dict["tar_mysql_database"] + " -e 'update " + self.m2_config_json["db"]["table_prefix"] + "core_config_data set value=\"" + self.settings_dict["tar_base_url"].split('https://')[1].split('/')[0] + "\" where path like \"%cookie_domain%\" AND scope_id=\"0\"'").read()
