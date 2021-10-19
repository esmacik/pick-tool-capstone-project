import splunklib.client as client
import splunklib.results as results
from ingestion.logentry import LogEntry


class SplunkInterface:

    def __init__(self, root_files, red_files, blue_files, white_files):
        self.root_files = root_files
        self.red_files = red_files
        self.blue_files = blue_files
        self.white_files = white_files

    # Get the splunk connection
    def connect(self):
        HOST = "localhost"
        PORT = 8089
        USERNAME = "binarybeasts101"
        PASSWORD = "#2020Utep"
        # Access scheme (default: https)
        scheme = "https"
        # Your version of Splunk (default: 5.0)
        version = 5.0

        # Create a Service instance and log in
        self.service = service = client.connect(
            host=HOST,
            port=PORT,
            username=USERNAME,
            password=PASSWORD)
        # Retrieve the index for the data
        self.index = self.service.indexes["test_splunk"]
        return self

    # Send files to splunk
    def start_ingestion(self):
        # trying to automatically ingest this
        # ingest = self.rootDirectory.text()
        #
        # print("Ingestion Complete!")
        # # Upload and index the file
        # self.index.upload(ingest)
        # print(self.index)

        self.ingest_files(self.root_files)
        self.ingest_files(self.red_files)
        self.ingest_files(self.blue_files)
        self.ingest_files(self.white_files)
        print("FINISHED INGESTION")

        return self

    def ingest_files(self, directory_files):
        if directory_files != "":
            for filepath in directory_files:
                self.index.upload(filepath)

    # Get a list of log entries from splunk
    def get_log_entries(self):
        # Run an export search and display the results using the results reader.

        # Set the parameters for the search:
        # - Search everything in the last hour
        # - Run a normal-mode search
        # - Search internal index
        kwargs_export = {"earliest_time": "-1000h",
                         "latest_time": "now",
                         "search_mode": "normal"}
        searchquery_export = "search index=test_splunk"

        exportsearch_results = self.service.jobs.export(searchquery_export, **kwargs_export)

        # Get the results and display them using the ResultsReader
        reader = results.ResultsReader(exportsearch_results)
        log_entries = []
        for result in reader:
            if isinstance(result, dict):
                # Add log entry to list
                print("Result: %s" % result)
                log_entry = LogEntry(result['_serial'],
                                     result['_raw'],
                                     result['_time'],
                                     result['index'],
                                     result['source'],
                                     result['sourcetype'])
                log_entries.append(log_entry)
            elif isinstance(result, results.Message):
                # Diagnostic messages may be returned in the results
                print("Message: %s" % result)

        # Print whether results are a preview from a running search
        print("is_preview = %s " % reader.is_preview)
        print("Found " + str(len(log_entries)) + " log entries.")
        return log_entries
