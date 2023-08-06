from incv_client.tof.wx_robot import WXRobotClient


class TofClient:
    def __init__(self, union):
        self.union = union

    @property
    def wx_robot(self):
        return WXRobotClient(self.union)
