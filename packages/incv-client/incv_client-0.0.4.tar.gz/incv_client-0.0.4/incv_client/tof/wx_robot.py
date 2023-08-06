from django.conf import settings


class WXRobotClient:
    def __init__(self, union):
        self.__union = union

    def send(self, data):
        url = "{}/tof/wx_robot/".format(self.__union.api_domain)
        data["rid"] = settings.INCV_API_WXROBOT_RID
        return self.__union.web.post(url, json=data).json()

    def send_text(self, content, mention_mobile_list=None, mention_all=False):
        if mention_mobile_list is None:
            mention_mobile_list = []
        if mention_all:
            mention_mobile_list.append("@all")
        data = {
            "msgtype": "text",
            "text": {"content": content, "mentioned_mobile_list": mention_mobile_list},
        }
        return self.send(data)

    def send_markdown(self, content):
        data = {"msgtype": "markdown", "markdown": {"content": content}}
        return self.send(data)

    def send_news(self, title, url, pic_url, desc=None):
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {"title": title, "description": desc, "url": url, "picurl": pic_url}
                ]
            },
        }
        return self.send(data)

    def send_card(self, data):
        return self.send(data)
