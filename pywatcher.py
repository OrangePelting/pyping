import subprocess
import platform
import logging
import json

from threading import Timer


class Host:
    """Represents a host on the network"""
    def __init__(self, ip: str, friendly_name: (str, None) = None):
        self.ip = ip
        self.friendly_name = friendly_name

    def get_config(self) -> dict:
        """
        Returns the HostMonitor's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return {"ip": self.ip, "friendly_name": self.friendly_name}


class Monitor:
    """
    Creates an object which periodically attempts to ping the specified Host.

        Parameters:
            target_host (Host): The host that will be monitored.
            interval (int): How many seconds between each ping attempt.
            tolerance (int): How many consecutive pings can the host miss before the monitor reports an anomaly.
            output_file (str): Path to the log file the monitor will output to.

    Downtime will be saved to the specified log file along with a timestamp
    """
    def __init__(self, target_host: Host, interval: int, tolerance: int, output_file: str):
        self.target_host = target_host
        self.interval = interval
        self.tolerance = tolerance
        self.output_file = output_file

        self._attempts = 0
        self._is_running = False

    def get_config(self) -> dict:
        """
        Returns the HostMonitor's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return {"target_host": Host.get_config(), "interval": self.interval, "tolerance": self.tolerance}

# todo: Add daemon threading.
# todo: Add pinging function.
# todo: Add functionality to allow watchers to be loaded from the watchers.json file.
