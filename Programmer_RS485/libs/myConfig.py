import configparser
import ast  # To safely convert string lists from INI file

class MyConfig:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # Read the configuration file
        self.load_config()

    def load_config(self):
        """Load configuration from the INI file."""
        self.config.read(self.config_file)

        # Ensure the [SETTINGS] section exists
        if "SETTINGS" not in self.config:
            self.config["SETTINGS"] = {}

    def get_compare_versions(self):
        """Return compareVersions as a boolean."""
        return self.config.getboolean("SETTINGS", "compareVersions", fallback=False)

    def get_slave_addresses(self):
        """Return slaveAddresses as a list of integers."""
        raw_value = self.config.get("SETTINGS", "slaveAddresses", fallback="[]")
        try:
            return ast.literal_eval(raw_value) if raw_value else []
        except (SyntaxError, ValueError):
            return []

    def get_notify_email(self):
        """Return notifyEmail as a string or None if empty."""
        email = self.config.get("SETTINGS", "notifyEmail", fallback="")
        return email if email else None

    def set_value(self, section, key, value):
        """Set a value in the configuration and save it."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)
        self.save_config()

    def save_config(self):
        """Write updated values back to the config file."""
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)  # <-- Fixed this line

# Example Usage
if __name__ == "__main__":
    config_handler = MyConfig("config.ini")

    # Read values from config
    print("Compare Versions:", config_handler.get_compare_versions())
    print("Slave Addresses:", config_handler.get_slave_addresses())
    print("Notify Email:", config_handler.get_notify_email())

    # Modify and save configuration
    config_handler.set_value("SETTINGS", "compareVersions", True)
    config_handler.set_value("SETTINGS", "slaveAddresses", [4, 5, 6])
    config_handler.set_value("SETTINGS", "notifyEmail", "newemail@example.com")

    print("Updated Compare Versions:", config_handler.get_compare_versions())
    print("Updated Slave Addresses:", config_handler.get_slave_addresses())
    print("Updated Notify Email:", config_handler.get_notify_email())
