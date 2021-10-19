from ingestion.logentry import LogEntry
from configuration.icon import Icon


class Node:

    def __init__(self, id, name, log_entry, icon = None):
        self.id = id
        self.name = name
        self.log_entry = log_entry
        self.icon = icon

    # Set the details of this node
    def set_details(self, id, name, log_entry, icon = None):
        self.id = id
        self.name = name
        self.log_entry = log_entry
        self.icon = icon

    # Get the name of this node
    def get_name(self):
        return self.name

    # Get this note's stored log entry.
    def get_log_entry(self):
        return self.log_entry

    # Get the icon associated with this node.
    def get_icon(self):
        return self.icon
