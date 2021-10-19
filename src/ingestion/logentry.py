class LogEntry:

    def __init__(self, id, data, time, source_index, source_file, source_type):
        self.id = id
        self.data = data
        self.time = time
        self.source_index = source_index
        self.source_file = source_file
        self.source_type = source_type

    # Set details for this log entry
    def set_details(self, id, data, time, source_index, source_file, source_type):
        self.id = id
        self.data = data
        self.time = time
        self.source_index = source_index
        self.source_file = source_file
        self.source_type = source_type

    # Print this log entry for debugging and logging
    def print(self):
        print("id: '%s', data: '%s', time: '%s', source_index: '%s', source_file: '%s', source_type: '%s'" %
              (self.id, self.data, self.time, self.source_index, self.source_file, self.source_type))

    # Get a dictionary representation of this Log Entry
    def to_dict(self):
        return {"_id": self.id,
                "data": self.data,
                "time": self.time,
                "source_index": self.source_index,
                "source_file": self.source_file,
                "source_type": self.source_type}
