from incv_client.tof.mail import MailClient
from incv_client.tof.sms import SMSClient
from incv_client.tof.wx_robot import WXRobotClient


class TofClient:
    def __init__(self, union):
        self.__union = union

    @property
    def wx_robot(self):
        return WXRobotClient(self.__union)

    @property
    def sms(self):
        return SMSClient(self.__union)

    @property
    def mail(self):
        return MailClient(self.__union)
