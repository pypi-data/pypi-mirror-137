from ShynaProcess import ShynaSpeak
import os
from ShynaDatabase import Shdatabase


class ShynaStartTest:
    s_process = ShynaSpeak.ShynaSpeak()
    s_data = Shdatabase.ShynaDatabase()
    s_data.device_id = "termux"

    def test_tts(self):
        msg = "hello" + str(os.environ.get("bossname"))
        self.s_process.shyna_speaks(msg=msg)
        self.s_data.set_date_system(process_name="termux_test")


if __name__ == '__main__':
    ShynaStartTest().test_tts()
