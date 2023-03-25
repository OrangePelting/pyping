class Host:
    """Represents a host on the network"""
    def __init__(self, ip: str, friendly_name: (str, None) = None):
        self.ip = ip
        self.friendly_name = friendly_name

    def pack(self) -> dict:
        """
        Returns the HostMonitor's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return {"ip": self.ip, "friendly_name": self.friendly_name}
