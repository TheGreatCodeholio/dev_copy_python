import os
from lib.text_color import Colors
import subprocess

def rsync_source_files(settings_dict):
    if os.path.exists(settings_dict["sou_public_html"]):
        child = subprocess.Popen("rm -rf " + settings_dict["sou_public_html"], shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        print(rc)
    print(Colors.OKGREEN + "RSYNC Source Files to Target." + Colors.ENDC)
    os.popen("rsync -Pav -e 'ssh -p " + settings_dict["sou_ssh_port"] + " -i " + settings_dict["sou_ssh_privkey_path"] + "' " + settings_dict["sou_ssh_user"] + "@" + settings_dict["sou_ssh_host"] + ":" + settings_dict["sou_public_html"] + " /srv/").read()