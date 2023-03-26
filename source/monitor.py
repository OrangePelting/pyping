import subprocess
import platform
from source import eventreporter
from threading import Thread
from time import sleep
from source.host import Host


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
    def __init__(self, target_host: Host, interval: int, tolerance: int,
                 output_file: str = "./logs/uptime.log", messages: [dict, None] = None):
        self.target_host = target_host
        self.interval = interval
        self.tolerance = tolerance

        self._output_file = output_file
        self._attempts = 0
        self._is_running = True
        self._run = False
        if messages is not None:
            self._logger = eventreporter.EventReporter(self.target_host, self._output_file, messages)
        else:
            self._logger = eventreporter.EventReporter(self.target_host, self._output_file)

    def pack(self) -> dict:
        """
        Returns the HostMonitor's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return {"target_host": self.target_host.pack(), "interval": self.interval,
                "tolerance": self.tolerance, "output_file": self._output_file, "logger": self._logger.pack()}

    def _ping(self):    # Thanks to all the kings and queens on stack overflow. Couldn't have done this without you!
        """Pings the target host"""
        if platform.system().lower() == "windows":
            pram = "-n"
        else:
            pram = "-c"

        # Builds the command
        command = ["ping", pram, "1", self.target_host.ip]
        if subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True):
            return False
        else:
            return True

    def _check_host(self):
        """Checks the host state and logs changes in the output file"""
        while True:
            if self._is_running:
                if self._ping():
                    self._attempts = 0
                else:
                    self._attempts += 1
                    if self._attempts > self.tolerance:
                        self._logger.log_host_down()
                        self._is_running = False
            else:
                if self._ping():
                    self._logger.log_host_up()
                    self._is_running = True
                    self._attempts = 0
            if not self._run:
                break
            sleep(self.interval)

    def start(self):
        """Starts the monitor"""
        self._run = True
        watcher = Thread(target=self._check_host, daemon=True)
        watcher.start()

    def stop(self):
        """Stops the monitor"""
        self._run = False

    def get_state(self) -> str:
        """Checks to see if the monitor is running and returns the state as a string"""
        if self._run:
            return "Running"
        else:
            return "Stopped"
