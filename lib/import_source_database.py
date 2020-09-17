import os
from lib.text_color import Colors


def import_source_database(settings_dict):

    # Check for old database, remove if it exists.
    if os.path.exists("/srv/backups/fixed_dump.sql"):
        os.popen("rm /srv/backups/fixed_dump.sql")
    # Fix SUPER Privs
    print(Colors.OKGREEN + "Fixing Super Privileges." + Colors.ENDC)
    os.popen("sed -E 's/DEFINER=`[^`]+`@`[^`]+`/DEFINER=CURRENT_USER/g' /srv/backups/db_" + settings_dict["date"] + ".sql > /srv/backups/fixed_dump.sql")
    # Drop Old Database
    os.popen("mysql -h mysql -u " + settings_dict["tar_mysql_user"] + " -p'" + settings_dict["tar_mysql_password"] + "' -e 'drop database " + settings_dict["tar_mysql_database"] + "'").read()
    # Create Blank Database
    os.popen("mysql -h mysql -u " + settings_dict["tar_mysql_user"] + " -p'" + settings_dict["tar_mysql_password"] + "' -e 'create database " + settings_dict["tar_mysql_database"] + "'").read()
    # Import Fixed Dump
    print(Colors.OKGREEN + "Importing Source Database to Target." + Colors.ENDC)
    os.popen("mysql -h mysql -u " + settings_dict["tar_mysql_user"] + " -p'" + settings_dict["tar_mysql_password"] + "' " + settings_dict["tar_mysql_database"] + " < /srv/backups/fixed_dump.sql").read()
    # Remove fixed database, keeping synced one for backup.
    os.popen("rm /srv/backups/fixed_dump.sql")
    # Finished Import