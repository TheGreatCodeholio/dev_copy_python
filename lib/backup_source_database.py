import os

from lib.text_color import Colors


def backup_source_database(settings_dict):
    # Get Remote Database Credentials via SSH
    print(Colors.OKGREEN + "Getting Source Database Credentials." + Colors.ENDC)
    dump_creds = os.popen("ssh -i " + settings_dict["sou_ssh_privkey_path"] + " " + settings_dict["sou_ssh_user"] + "@" + settings_dict["sou_ssh_host"] + " -p" + settings_dict["sou_ssh_port"] + " '/usr/share/stratus/cli database.config > cred.log 2>&1; cat cred.log'").read()
    os.popen("ssh -i " + settings_dict["sou_ssh_privkey_path"] + " " + settings_dict["sou_ssh_user"] + "@" + settings_dict["sou_ssh_host"] + " -p" + settings_dict["sou_ssh_port"] + " 'rm cred.log'")
    cred_file = open("remote_creds.log", "w")
    cred_file.write(dump_creds)
    cred_file.close()
    # Read Credentials to our settings Dictionary
    settings_dict["sou_mysql_user"] = os.popen("cat remote_creds.log | grep Username | awk '{print $3}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    settings_dict["sou_mysql_database"] = os.popen("cat remote_creds.log | grep Username | awk '{print $7}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    settings_dict["sou_mysql_password"] = os.popen("cat remote_creds.log | grep Username | awk '{print $14}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    os.popen("rm remote_creds.log")
    # MySQL Dump Database
    print(Colors.OKGREEN + "Dumping Source Database." + Colors.ENDC)
    os.popen("ssh -i " + settings_dict["sou_ssh_privkey_path"] + " " + settings_dict["sou_ssh_user"] + "@" + settings_dict["sou_ssh_host"] + " -p" + settings_dict["sou_ssh_port"] + " 'mysqldump --skip-lock-tables --extended-insert=FALSE --verbose -h mysql --quick -u " + settings_dict["sou_mysql_user"] + " -p" + settings_dict["sou_mysql_password"] + " " + settings_dict["sou_mysql_database"] + " > /srv/db_" + settings_dict["date"] + ".sql'").read()
    # Check if backups directory exists locally
    if not os.path.exists("/srv/backups"):
        os.popen("mkdir /srv/backups")
    # RSYNC Database Dump to Local backups folder.
    print(Colors.OKGREEN + "RSYNC Source Database to Target." + Colors.ENDC)
    os.popen("rsync -Pav -e 'ssh -p " + settings_dict["sou_ssh_port"] + " -i " + settings_dict["sou_ssh_privkey_path"] + "' " + settings_dict["sou_ssh_user"] + "@" + settings_dict["sou_ssh_host"] + ":/srv/db_" + settings_dict["date"] + ".sql /srv/backups/").read()
    # Finished with databse backup.