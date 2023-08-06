import os
from Shynatime import ShTime
from ShynaDatabase import Shdatabase
import random


class ShynaRun:
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    command = ''
    response = None

    def run_cmd_with_response(self, command):
        self.command = command
        try:
            self.response = os.popen(str(self.command)).read()
            self.response = eval(self.response)
        except Exception as e:
            print(e)
            self.response = str(e)
        finally:
            return self.response

    def start_run(self):
        try:
            cmd = "termux-dialog speech"
            call = self.run_cmd_with_response(command=cmd)['text']
            if "" == call:
                sent = ["hello", "Hey", "Yes, tell me", "I am here", "I am busy", "yes, I am here", "hey!",
                        "yep,tell me", "sorry, what?!"]
                choice = "termux-tts-speak -s ALARM '" + random.choice(sent) + "'"
                os.popen(choice)
            else:
                cmd = "termux-toast " + str(call) + ""
                os.popen(cmd)
                self.s_data.query = "INSERT INTO TTM_sent (task_date, task_time, sent) VALUES('" + str(
                    self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" + str(call).lower() + "')"
                insert_status = self.s_data.insert_or_update_or_delete_with_status()
                if insert_status is True:
                    sent = ["Roger that", "Consider it done", "I got your back", "got it", "sure", "okay! processing",
                            "what will you without me?!", "ahan!"]
                    choice = "termux-tts-speak -s ALARM '" + random.choice(sent) + "'"
                    os.popen(choice)
                else:
                    sent = ["something went wrong", "did not worked", "please, try again", "nope, try again",
                            "Exception alert?!", "I ran into error"]
                    choice = "termux-tts-speak -s ALARM '" + random.choice(sent) + "'"
                    os.popen(choice)
        except Exception as e:
            sent = ["something went wrong", "did not worked", "please, try again", "nope, try again",
                    "Exception alert?!", "I ran into error"]
            choice = "termux-tts-speak -s ALARM '" + random.choice(sent) + "'"
            os.popen(choice)
            print(e)


if __name__ == '__main__':
    ShynaRun().start_run()
