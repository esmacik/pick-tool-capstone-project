class Icon:

    def __init__(self, name, source):
        self.name = name
        self.source = source

    # Set the name of this icon
    def set_name(self, name):
        self.name = name

    # Set the source for this icon
    def set_source(self, source):
        self.source = source

    # Get the name for this icon
    def get_name(self):
        return self.name

    # Get the source for this icon
    def get_source(self):
        return self.source

    # Get a dictionary representation of this icon
    def get_dict(self):
        return {"name": self.name,
                "source": self.source}