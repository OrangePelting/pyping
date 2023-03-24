import subprocess
import platform
import eventreporter
import json

from threading import Timer

from host import Host


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
        self._logger = eventreporter.EventReporter(self.target_host, "./pywatch.log")

    def pack(self) -> dict:
        """
        Returns the HostMonitor's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return {"target_host": self.target_host.pack(), "interval": self.interval,
                "tolerance": self.tolerance, "logger": self._logger}

    def _ping(self):
        if platform.system().lower() == "windows":
            pram = "-n"
        else:
            pram = "-c"

        command = ["ping", pram, "1", self.target_host.ip]
        output = subprocess.call(command)
        if output == 1 or "Destination host unreachable" in output:
            return False
        else:
            return True

# todo: Add daemon threading.
# todo: Add... ya know.. a pinging function?
# todo: Add functionality to allow watchers to be loaded from the watchers.json file.
