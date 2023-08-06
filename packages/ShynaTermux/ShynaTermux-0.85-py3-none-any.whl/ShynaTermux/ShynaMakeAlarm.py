import os
from Shynatime import ShTime
from ShynaDatabase import Shdatabase
from ShynaProcess import ShynaSpeak
import re
import multiprocessing


# Todo: Can put the regex code in process package


class ShynaMakeAlarm:
    s_time = ShTime.ClassTime()
    s_data = Shdatabase.ShynaDatabase()
    s_process = ShynaSpeak.ShynaSpeak()
    reminder_date = s_time.now_date
    reminder_time = s_time.now_time
    response = None

    def make_alarm(self, call):
        try:
            regex = r"(wake me up at)"
            matches = re.finditer(regex, call.lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    call = self.s_time.check_am_pm(text_string=call)
                    status, self.reminder_date, self.reminder_time = self.s_time.get_date_and_time_for_alarm(text_string=call)
                    print("setting Alarm for", self.reminder_date, self.reminder_time)
                else:
                    pass
            regex = r"(let me know when it is)"
            matches = re.finditer(regex, call.lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    call = self.s_time.check_am_pm(text_string=call)
                    status, self.reminder_date, self.reminder_time = self.s_time.get_date_and_time_for_alarm(text_string=call)
                    print("setting Alarm for", self.reminder_date, self.reminder_time)
                else:
                    pass
            regex = r"(alarm)"
            matches = re.finditer(regex, call.lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    call = self.s_time.check_am_pm(text_string=call)
                    status, self.reminder_date, self.reminder_time = self.s_time.get_date_and_time_for_alarm(text_string=call)
                else:
                    pass
            alarm_title = "Setting up Alarm for " + self.reminder_date + " " + self.reminder_time
            command = "termux-toast -g top " + alarm_title
            os.popen(cmd=command)
            if call.lower().__contains__('let me know'):
                status = "no"
            else:
                multiprocessing.Process(target=self.s_process.shyna_speaks_termux(msg="Want to setup repeat?")).start()
                status = str(self.run_cmd_with_response(command="termux-dialog speech")['text']).lower()
            if status.__contains__('no'):
                self.s_data.query = "INSERT INTO alarm (task_date, task_time, alarm_title, alarm_date, alarm_time, " \
                                    "snooze_status, snooze_duration, repeat_status ,repeat_frequency, alarm_status) " \
                                    "VALUES ('" + str(self.s_time.now_date) + "', '" \
                                    + str(self.s_time.now_time) + "', '" + str(alarm_title) + "', '" \
                                    + str(self.reminder_date) + "', '" + str(self.reminder_time) + "', 'TRUE', " \
                                                                                                   "'15', 'False', " \
                                                                                                   "'Never', 'TRUE')"
                multiprocessing.Process(target=self.s_data.create_insert_update_or_delete()).start()
                multiprocessing.Process(target=self.s_process.shyna_speaks_termux(msg="consider it done"))
            else:
                command = "termux-dialog spinner -t 'select duration' -v 'Daily, Weekends, Weekdays, Alternative, Never'"
                snooze = str(self.run_cmd_with_response(command=command)['text']).lower()
                self.s_data.query = "INSERT INTO alarm (task_date, task_time, alarm_title, alarm_date, alarm_time, " \
                                    "snooze_status, snooze_duration, repeat_frequency, alarm_status) VALUES ('" \
                                    + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" \
                                    + str(alarm_title) + "', '" + str(self.reminder_date) + "', '" \
                                    + str(self.reminder_time) + "', 'TRUE', '15', '" + str(snooze) + "', 'TRUE')"
                multiprocessing.Process(target=self.s_data.create_insert_update_or_delete()).start()
                multiprocessing.Process(target=self.s_process.shyna_speaks_termux(msg="consider it done"))
        except Exception as e:
            self.s_process.shyna_speaks_termux(msg="Ops! this is broken")
            print(e)

    def run_cmd_with_response(self, command, priority=None):
        try:
            if priority is None:
                priority = 1
            if priority == 1:
                self.response = os.popen(str(command)).read()
                self.response = eval(self.response)
            else:
                self.s_process.updated_speak_or_not_status(status=True)
                self.response = os.popen(str(command)).read()
                self.response = eval(self.response)
        except Exception as e:
            print(e)
            self.response = str(e)
        finally:
            return self.response

    def initiate_interaction(self):
        try:
            morning_list = ['good morning', 'morning', 'i am up', 'look alive', 'hey']
            night_list = ['good night', 'night', 'i am sleeping', 'sleep', 'go to sleep']
            if str(self.s_process.speak_or_not()).lower().__eq__('awake'):
                command = "termux-dialog speech -t 'Hey, you are talking to Shyna' -i 'Tell me, how can I help?'"
            else:
                command = "termux-dialog speech -t 'Hey, you are talking to Shyna' -i 'I will be quite, I promise.'"
            response = str(self.run_cmd_with_response(command=command)['text']).lower()
            print(response)
            if len(response) > 0:
                if str(response).__contains__('alarm') and str(response).__contains__('set'):
                    self.make_alarm(response)
                elif str(response).__contains__('wake me up at'):
                    self.make_alarm(response)
                elif str(response).__contains__('let me know'):
                    self.make_alarm(response)
                elif str(response) in morning_list:
                    self.s_process.updated_speak_or_not_status(status=True)
                elif str(response) in night_list:
                    self.s_process.updated_speak_or_not_status(status=False)
                else:
                    self.create_notification()
            else:
                command = "Can you please speak little loud or go for the option below"
                self.s_process.shyna_speaks_termux(msg=command)
                self.create_notification()
        except Exception as e:
            command = "termux-toast " + str(e)
            os.popen(cmd=command)
            print(e)
            self.create_notification()

    def create_notification(self):
        try:
            command = str(self.run_cmd_with_response("termux-dialog text -t 'Please enter string having time'")['text'])
            self.make_alarm(call=command)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    ShynaMakeAlarm().initiate_interaction()

