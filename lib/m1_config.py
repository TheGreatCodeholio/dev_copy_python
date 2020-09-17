import os
import subprocess as sp
from pyexpat import ExpatError
import lib.xmltodict as xmltodict
import json

from lib.text_color import Colors

class m1_config:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict
        self.m1_config_json = {}
        self.prefix = 0
        self.init_config()

    def init_config(self):
        if not os.path.exists(self.settings_dict["sou_public_html"] + "/app/etc/local.xml"):
            print(Colors.FAIL + "Magento 1 Configuration doesn't exist, exiting" + Colors.ENDC)
            exit(1)
        with open(self.settings_dict["sou_public_html"] + "/app/etc/local.xml", "r") as f:
            data = f.read()
            f.close()
        try:
            doc = xmltodict.parse(data)
            config = json.dumps(doc)
            self.m1_config_json = json.loads(config)
        except ExpatError:
            doc = xmltodict.parse(data[2:])
            config = json.dumps(doc)
            self.m1_config_json = json.loads(config)

        if self.m1_config_json["config"]["global"]["resources"]["db"]["table_prefix"] == None:
            self.prefix = ""
        else:
            self.prefix = self.m1_config_json["config"]["global"]["resources"]["db"]["table_prefix"]
        print(self.m1_config_json)
        self.configure_database()

    def configure_database(self):
        print(Colors.OKGREEN + "Configuring Database." + Colors.ENDC)
        child = sp.Popen("sed -i -e '/                    <username><.*/c\                    <username><![CDATA[" + self.settings_dict["tar_mysql_user"] + "]]></username>' " + self.settings_dict["sou_public_html"] + "/app/etc/local.xml", shell=True, stdout=sp.PIPE)
        output = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(Colors.FAIL + "Changing local.xml config failed")

        child = sp.Popen("sed -i -e '/                    <password><.*/c\                    <password><![CDATA[" + self.settings_dict["tar_mysql_password"] + "]]></password>' " + self.settings_dict["sou_public_html"] + "/app/etc/local.xml", shell=True, stdout=sp.PIPE)
        output = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(Colors.FAIL + "Changing local.xml config failed")

        child = sp.Popen("sed -i -e '/                    <dbname><.*/c\                    <dbname><![CDATA[" + self.settings_dict["tar_mysql_database"] + "]]></dbname>' " + self.settings_dict["sou_public_html"] + "/app/etc/local.xml", shell=True, stdout=sp.PIPE)
        output = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(Colors.FAIL + "Changing local.xml config failed")
        self.update_base_url()

    def update_base_url(self):
        print(Colors.OKGREEN + "Updating Base URL" + Colors.ENDC)
        child = sp.Popen("mysql -h mysql -u " + self.settings_dict["tar_mysql_user"] + " -p\"" + self.settings_dict["tar_mysql_password"] + "\" " + self.settings_dict["tar_mysql_database"] + " -e 'update " + str(self.prefix) + "core_config_data set value=\"" + self.settings_dict["tar_base_url"] + "\" where path like \"web/%secure/base_url\" AND scope=\"default\"'", shell=True, stdout=sp.PIPE)
        output = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(Colors.FAIL + "Changing Database Base URL failed.")
        else:
            print(Colors.OKGREEN + "Success")
        self.update_cookie_domain()

    def update_cookie_domain(self):
        print(Colors.OKGREEN + "Updating Cookie Domain" + Colors.ENDC)
        child = sp.Popen("mysql -h mysql -u " + self.settings_dict["tar_mysql_user"] + " -p\"" + self.settings_dict["tar_mysql_password"] + "\" " + self.settings_dict["tar_mysql_database"] + " -e 'update " + str(self.prefix) + "core_config_data set value=\"" + self.settings_dict["tar_base_url"].split('https://')[1].split('/')[0] + "\" where path like \"%cookie_domain%\" AND scope_id=\"0\"'", shell=True, stdout=sp.PIPE)
        output = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(Colors.FAIL + "Changing Database Base URL failed.")
        else:
            print(Colors.OKGREEN + "Success")



