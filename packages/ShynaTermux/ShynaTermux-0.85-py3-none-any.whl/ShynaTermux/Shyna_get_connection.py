from Shynatime import ShTime
from ShynaDatabase import Shdatabase
import os


class ShynaConnection:
    result = ""
    wifi_home_name = 'shivam'
    s_time = ShTime.ClassTime()
    s_data = Shdatabase.ShynaDatabase()
    s_data.device_id = "termux"

    def check_wifi(self):
        self.result = 'phone'
        try:
            wifi_info = os.popen('termux-wifi-connectioninfo').read()
            if str(wifi_info).lower().__contains__(self.wifi_home_name):
                self.result = 'home'
                self.s_data.query = "INSERT INTO connection_check (connection_type, from_application, new_date, new_time)" \
                                    " VALUES ('" + str(self.result) + "','" + str(self.s_data.device_id) + "','" \
                                    + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "')"
                self.s_data.create_insert_update_or_delete()
            else:
                self.result = 'phone'
                self.s_data.query = "INSERT INTO connection_check (connection_type, from_application, new_date, new_time)" \
                                    " VALUES ('" + str(self.result) + "','" + str(self.s_data.device_id) + "','" \
                                    + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "')"
                self.s_data.create_insert_update_or_delete()
        except Exception as e:
            print(e)
        finally:
            self.s_data.set_date_system(process_name="connection_check")
            return self.result


if __name__ == '__main__':
    ShynaConnection().check_wifi()
