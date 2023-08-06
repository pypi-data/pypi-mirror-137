import nltk
import os


class ShynaTermuxSetup:
    """We need setup few things to make it work and test"""
    case_env = ''

    def set_env_variable(self):
        try:
            self.case_env = input("Want to add Environment (y/n)")
            if self.case_env.__contains__('yes') or self.case_env.__contains__('y'):
                dbhost = input("Enter the database host")
                dbhost_cmd = "echo 'export host=" + dbhost + "'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
                dbpasswd = input("Enter the database password")
                dbhost_cmd = "echo 'export passwd=" + dbpasswd + "'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
                dbhost_cmd = "echo 'export bossname=Shivam'>>~/.bash_profile;"
                os.popen(dbhost_cmd).readlines()
                ftpuser = input("Enter the ftp user")
                ftpuser_cmd = "echo 'export ftpuser=" + ftpuser + "'>>~/.bash_profile;"
                os.popen(ftpuser_cmd).readlines()
                ftppasswd = input("Enter the ftp passwd")
                ftpcmd = "echo 'export ftpasswd=" + ftppasswd + "'>>~/.bash_profile;"
                os.popen(ftpcmd).readlines()
                os.popen('wget -r --ftp-user="'+ftpuser+'" --ftp-password="'+ftppasswd+'" ftp://www.shyna623.com/termux')
            else:
                pass
            self.case_env = input("Want to install remaining (y/n)")
            if self.case_env.__contains__('yes') or self.case_env.__contains__('y'):
                os.popen("pkg install sox --assume-yes").readline()
                os.popen("pkg install termux-api --assume-yes").readline()
                # os.popen('+')
                dbhost_cmd = """termux-notification --on-delete 'termux-tts-speak "hey Shivam"' -t 'Hey Shivam' """
                os.popen(dbhost_cmd)
                nltk.download('all')
            else:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ShynaTermuxSetup().set_env_variable()
