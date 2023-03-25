from datetime import datetime
import json
import logging
from source.host import Host

# Set the logging level for my own debugging
logging.basicConfig(level=0)
# todo: remove this and hope nobody realizes you wasted a bunch of time on your own logging function

# Set the default log messages.
with open("./source/default_messages.json", "r") as j:
    default_messages = json.load(j)


def get_timestamp() -> str:
    """Returns the date and time in local time. Style:('yyyy-mm-dd -- HH:MM:SS')"""
    logging.debug("Fetched time")
    return datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")


def get_utc_timestamp() -> str:
    """Returns the date and time in UTC time. 'Style:('yyyy-mm-dd -- HH:MM:SS')"""
    logging.debug("Fetch UTC time")
    return datetime.utcnow().strftime("%Y-%m-%d -- %H:%M:%S")


# This is going to be the class used to create logs and enter them in log files.
class EventReporter:
    """
    Creates logs and appends them to the specified log file.
        Parameters:
            host (monitor.Host): The host device.
            output_file (str): The log file to save logs to.
            messages (dict): The message segments that will be used in log entries
    """

    def __init__(self, host: Host, output_file: str, messages=default_messages):
        if messages is None:
            messages = default_messages.copy()
        logging.debug("Created Logger")

        self.path_to_output_file = output_file
        self.ip = host.ip
        self.friendly_name = host.friendly_name
        self._message_segments = messages.copy()

    def _friendly_name_or_ip(self) -> str:
        """Uses the host's ip address in place of the friendly name if no friendly name is provided"""
        if self.friendly_name is None:
            return self.ip
        else:
            return self.friendly_name

    def _friendly_name(self) -> str:  # todo: there is probably a better way to do this.
        """Returns friendly name or empty string if friendly name is not provided"""
        if self.friendly_name is None:
            return ""
        else:
            return self.friendly_name

    # This does error checking in case the user-entered message segments have invalid keys.
    # todo: Maybe split this into two different methods.
    def _add_dynamic_content(self, key: str) -> str:
        """
        Inserts dynamic content into message the message segments.

            Parameters:
                key (str): Message segment address in _messages dictionary.
        """
        try:    # This will work if you use the program correctly
            logging.debug("Attempting to add dynamic content")
            return self._message_segments[key].format(
                UTC_TIMESTAMP=get_utc_timestamp(),
                TIMESTAMP=get_timestamp(),
                FRIENDLY_NAME=self._friendly_name(),
                FRIENDLY_NAME_OR_IP=self._friendly_name_or_ip(),
                IP=self.ip)
        except KeyError as error:    # This will only occur with user error
            logging.error(f"Failed to add dynamic content {error}")
            self._message_segments[key] = default_messages[key]
            return str(f"Key Error found in {key}! Reset {key} to default"    # The indentation.. It's so ugly
                       + self._message_segments[key].format(
                            UTC_TIMESTAMP=get_utc_timestamp(),
                            TIMESTAMP=get_timestamp(),
                            FRIENDLY_NAME=self._friendly_name(),
                            FRIENDLY_NAME_OR_IP=self._friendly_name_or_ip(),
                            IP=self.ip))

    def _log_entry_head(self) -> str:
        """Returns log_entry_head with dynamic content added."""
        return self._add_dynamic_content("log_entry_head")

    def _log_entry_tail(self) -> str:
        """Returns log_entry_tail with dynamic content added."""
        return self._add_dynamic_content("log_entry_tail")

    def _host_down_message(self) -> str:
        """Returns host_down_message with dynamic content added."""
        return self._add_dynamic_content("host_down_message")

    def _host_up_message(self) -> str:
        """Returns host_up_message with dynamic content added."""
        return self._add_dynamic_content("host_up_message")

    # todo: Maybe keep this? If so, add a docstring.
    def _test_dynamic_content(self):
        logging.debug("Testing logs with dynamic content!")
        print(self._log_entry_head(), self._host_up_message(), self._log_entry_tail(), )
        print(self._log_entry_head(), self._host_down_message(), self._log_entry_tail())

    def pack(self) -> dict:
        """
        Returns the Logger's configuration as a dictionary which can easily be saved in a .json file.
        eg: {}
        """
        return self._message_segments

    def log_host_down(self):
        logging.debug("Logged host down")
        with open(self.path_to_output_file, 'a+') as a:
            a.write(self._log_entry_head() + self._host_down_message() + self._log_entry_tail())

    def log_host_up(self):
        logging.debug("Logged host up.")
        with open(self.path_to_output_file, 'a+') as a:
            a.write(self._log_entry_head() + self._host_up_message() + self._log_entry_tail())
