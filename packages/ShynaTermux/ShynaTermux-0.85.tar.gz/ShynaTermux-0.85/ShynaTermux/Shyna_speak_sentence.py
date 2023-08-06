from ShynaDatabase import Shdatabase
from ShynaProcess import ShynaSpeak


class ShynaSpeakOnTermux:
    """
    Get sentences from database and speak them as needed
    """
    s_data = Shdatabase.ShynaDatabase()
    s_process = ShynaSpeak.ShynaSpeak()

    def get_sentences(self):
        try:
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ShynaSpeakOnTermux().get_sentences()
