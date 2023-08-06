class SMSClient:
    def __init__(self, union):
        self.__union = union

    def send(self, phone: str, tid: str, params: list = None):
        url = "{}/tof/sms/".format(self.__union.api_domain)
        data = {"phone": phone, "tid": tid, "params": params}
        return self.__union.web.post(url, json=data).json()
