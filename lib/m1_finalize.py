import os
from lib.text_color import Colors
import subprocess


class m1_finalize:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict

    def reindex(self):
        print(Colors.OKGREEN + "Starting Reindex." + Colors.ENDC)
        child = subprocess.Popen("php " + self.settings_dict["sou_public_html"] + "/shell/indexer.php --reindexall", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(streamdata.decode("UTF-8"))
            print(Colors.FAIL + "Reindex Failed." + Colors.ENDC)
        else:
            self.flush_cache()

    def flush_cache(self):
        print(Colors.OKGREEN + "Flushing Magento Cache" + Colors.ENDC)
        child = subprocess.Popen("rm -rf " + self.settings_dict["sou_public_html"] + "/var/cache", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(streamdata.decode("UTF-8"))
            print(Colors.FAIL + "Magento Cache Flush Failed." + Colors.ENDC)
        else:
            print(Colors.OKGREEN + "Success" + Colors.ENDC)

        print(Colors.OKGREEN + "Flushing Stratus Cache" + Colors.ENDC)
        child = subprocess.Popen("/usr/share/stratus/cli cache.all.clear", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            print(streamdata.decode("UTF-8"))
            print(Colors.FAIL + "Stratus Cache Flush Failed." + Colors.ENDC)
        else:
            print(Colors.OKGREEN + "Success" + Colors.ENDC)