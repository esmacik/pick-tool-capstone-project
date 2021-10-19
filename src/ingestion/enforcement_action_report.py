from ingestion.cleansing import Cleansing
from ingestion.validation import Validation


class EnforcementActionReport:

    def __init__(self):
        pass

    # Get log files that should be displayed in this EAR
    def get_log_files(self, source):
        pass

    # Get cleansing status to display in EAR
    def get_cleansing_status(self, source):
        pass

    # Get validation status to display in the EAR
    def get_validation_status(self, source):
        pass

    # Get ingestion status to display in this EAR
    def get_ingestion_status(self, source):
        pass

    # Get error description to show in EAR
    def get_error_description(self, source, log_error):
        pass
