from Shynatime import ShTime
from ShynaDatabase import Shdatabase
import os


class ShynaLocation:
    result = ""
    s_time = ShTime.ClassTime()
    s_data = Shdatabase.ShynaDatabase()
    s_data.device_id = "termux"

    def get_location(self):
        self.result = "Empty location"
        try:
            my_cmd = os.popen('termux-location -p network').read()
            if str(my_cmd) != '':
                new_dict = eval(my_cmd)
                new_latitude = new_dict['latitude']
                new_longitude = new_dict['longitude']
                new_altitude = new_dict['altitude']
                new_accuracy = new_dict['accuracy']
                new_vertical_accuracy = new_dict['vertical_accuracy']
                new_bearing = new_dict['bearing']
                new_speed = new_dict['speed']
                new_elapsedMS = new_dict['elapsedMs']
                new_provider = new_dict['provider']
                new_date = str(self.s_time.now_date)
                new_time = str(self.s_time.now_time)
                self.s_data.query = "INSERT INTO shivam_device_location(new_date, new_time, new_latitude, " \
                                    "new_longitude, new_altitude, new_accuracy, new_vertical_accuracy, new_bearing, " \
                                    "new_speed, new_elapsedMS, new_provider) VALUES ('" + str(new_date) + "','" \
                                    + str(new_time) + "', '" + str(new_latitude) + "', '" + str(new_longitude) + "', '" \
                                    + str(new_altitude) + "', '" + str(new_accuracy) + "', '" \
                                    + str(new_vertical_accuracy) + "', '" + str(new_bearing) + "', '" \
                                    + str(new_speed) + "', '" + str(new_elapsedMS) + "','" + str(new_provider) + "')"
                self.s_data.create_insert_update_or_delete()
                self.result = "Got Location"
            else:
                self.result = "Empty location"
        except Exception as e:
            print(e)
            self.result = "Exception"
        finally:
            self.s_data.set_date_system(process_name='location_check')
            return self.result


if __name__ == '__main__':
    ShynaLocation().get_location()
