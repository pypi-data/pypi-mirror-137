class MailClient:
    def __init__(self, union):
        self.__union = union

    def send(self, receivers: list, title: str, content: str, mail_type: str = None):
        mail_type = "html" if mail_type == "html" else "plain"
        url = "{}/tof/mail/".format(self.__union.api_domain)
        data = {
            "receivers": receivers,
            "title": title,
            "content": content,
            "mail_type": mail_type,
        }
        return self.__union.web.post(url, json=data).json()
