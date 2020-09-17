import os
from datetime import datetime, date, time, timezone
from lib.text_color import Colors
import subprocess
import json


class m2_finalize:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict

    def reindex(self):
        child = subprocess.Popen("php " + self.settings_dict["sou_public_html"] + "/bin/magento indexer:reindex", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(streamdata.decode("UTF-8"))
        else:
            self.flush_cache()

    def flush_cache(self):
        os.popen("php " + self.settings_dict["sou_public_html"] + "/bin/magento cache:clean")
        os.popen("/usr/share/stratus/cli cache.all.clear")