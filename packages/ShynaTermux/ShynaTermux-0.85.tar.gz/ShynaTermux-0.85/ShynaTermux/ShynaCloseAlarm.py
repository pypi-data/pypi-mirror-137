import os
from ShynaDatabase import Shdatabase
from Shynatime import ShTime


class CloseAlarm:
    s_time = ShTime.ClassTime()
    s_data = Shdatabase.ShynaDatabase()

    def close_alarm(self):
        try:
            self.s_data.query = "SELECT count, task_status FROM Task_Manager WHERE task_status = 'running'"
            result = self.s_data.select_from_table()
            print(result, type(result))
            if "Empty" in result:
                print("No")
                os.popen("termux-tts-speak 'Hey, Shiv! You have not set any alarm?!'")
            else:
                for row in result:
                    status = row[1]
                    count = row[0]
                    if str(status).lower().__eq__('running'):
                        print(status)
                        self.s_data.query = "UPDATE Task_Manager SET snooze_duration = '0', task_status='completed' " \
                                            "WHERE count = '" + str(count) + "'"
                        self.s_data.create_insert_update_or_delete()
                        self.s_data.query = "UPDATE Task_Manager SET snooze_duration = '0' WHERE count = '" \
                                            + str(count) + "'"
                        self.s_data.create_insert_update_or_delete()
                        os.popen("termux-tts-speak 'Hi, Closing alarm'")
                        self.s_data.query = "SELECT sunrise from weather_table where task_date = '" \
                                            + str(self.s_time.now_date) + "'"
                        result = self.s_data.select_from_table()
                        if "Empty" in result:
                            pass
                        else:
                            for item in result[0]:
                                if self.s_time.string_to_time(time_string=self.s_time.now_time) <= self.s_time.string_to_time(time_string=item):
                                    self.lights_on()
                                else:
                                    pass
                    else:
                        os.popen("termux-tts-speak 'Hey, Shiv! You have not set any alarm?!'")
        except Exception as e:
            print(e)

    def lights_on(self):
        cmd = "termux-torch on"
        self.s_data.query = "INSERT INTO shyna_termux (task_date, task_time, command_to_run) VALUES ('" \
                            + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" + str(cmd) + "')"
        print(self.s_data.query)
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "INSERT INTO shyna_rasp (task_date, task_time, command_to_run) VALUES('" \
                            + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" \
                            + str("speak:Good Morning") + "')"
        self.s_data.create_insert_update_or_delete()


if __name__ == '__main__':
    CloseAlarm().close_alarm()
