class ParlatyleInterface:

    def __init__(self):
        pass

    # Get files that need to be transcribed.
    def get_files(self, source):
        pass

    # Send the file at the source for transcription
    def transcribe(self, source):
        pass

    # Get files that have been transcribed
    def get_transcribed_files(self, source):
        pass
