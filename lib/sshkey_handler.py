from lib.text_color import Colors
import os


def ssh_key(ssh_user):
    if os.path.exists("/srv/.ssh/" + ssh_user):
        print(Colors.OKBLUE + "Key Exists for " + Colors.OKGREEN + ssh_user + Colors.ENDC)
        return "/srv/.ssh/" + ssh_user
    else:
        print(Colors.WARNING + "Creating Key for " + Colors.OKGREEN + ssh_user + Colors.ENDC)
        os.popen("ssh-keygen -t rsa -N \"\" -f ~/.ssh/" + ssh_user).read()
        return "/srv/.ssh/" + ssh_user
