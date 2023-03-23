from datetime import datetime


def get_timestamp() -> str:
    """Returns the date and time in local time. Style:('yyyy-mm-dd -- HH:MM:SS')"""
    return datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")


def get_utc_timestamp() -> str:
    """Returns the date and time in UTC time. 'Style:('yyyy-mm-dd -- HH:MM:SS')"""
    return datetime.utcnow().strftime("%Y-%m-%d -- %H:%M:%S")


default_messages = {
    "log_entry_head": "[{UTC_TIMESTAMP}]:",
    "log_entry_tail": "",
    "host_down_message": "{FRIENDLY_NAME} | {IP} is down!",
    "host_up_message": "{FRIENDLY_NAME} | {IP} is up!"
}


# This is going to be the class used to create logs and enter them in log files.
class Log:
    """
    Creates logs and appends them to the specified log file.
        Parameters:
            ip (str): The IP of the host device.
            friendly_name (str): Friendly name of host device.
            output_file (str): The log file to save logs to.
    """

    def __init__(self, ip: str, friendly_name: [str, None], output_file: str):
        # These attributes are set during the creation of the object.
        # unpack() will not modify these attributes.
        self.path_to_output_file = output_file
        self.ip = ip
        self.friendly_name = friendly_name
        # Holds message segments with dynamic content.
        self._message_segments = {
            "log_entry_head": default_messages["log_entry_head"],
            "log_entry_tail": default_messages["log_entry_tail"],
            "host_down_message": default_messages["host_down_message"],
            "host_up_message": default_messages["host_up_message"]}

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
            return self._message_segments[key].format(
                UTC_TIMESTAMP=get_utc_timestamp(),
                TIMESTAMP=get_timestamp(),
                FRIENDLY_NAME=self._friendly_name(),
                FRIENDLY_NAME_OR_IP=self._friendly_name_or_ip(),
                IP=self.ip)
        except KeyError:    # This will only occur with user error
            self._message_segments[key] = default_messages[key]
            return str(f"Key Error found in {key}! Resetting to default"    # The indentation.. It's so ugly
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
        print(self._log_entry_head(), self._host_up_message(), self._log_entry_tail(), )
        print(self._log_entry_head(), self._host_down_message(), self._log_entry_tail())

# todo: add pack and unpack functions so that custom log templates can be loaded into the logger object.
# todo: add host_up and host_down functions to make entries to the log.
