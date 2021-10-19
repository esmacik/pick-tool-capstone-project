import os
from configuration.vector import Vector
from configuration.icon import Icon
from ingestion.splunk_interface import SplunkInterface
from threading import Thread
from configuration.database_writer import DatabaseWriter
from ingestion.logentry import LogEntry


class Configuration:
    __instance = None

    @staticmethod
    def get_instance():
        if Configuration.__instance is None:
            Configuration.__instance = Configuration()
        return Configuration.__instance

    def __init__(self):
        self.is_lead = False
        self.lead_IP = "0.0.0.0"
        self.established_connections = 0

        self.event_name = ""
        self.event_description = ""
        self.event_start = ""
        self.event_end = ""

        self.root_directory = ""
        self.red_directory = ""
        self.blue_directory = ""
        self.white_directory = ""

        self.vectors = []
        self.icons = []
        self.splunk = None

        self.check_database()

        Configuration.__instance = self

    # look at database to see if there is information stored
    def check_database(self):
        lead_info = DatabaseWriter.get_all_documents_in_collection(DatabaseWriter.COLLECTION_TEAM)
        if len(lead_info) != 0:
            document = lead_info[0]
            print(str(document))
            self.is_lead = document["is_Lead"]
            self.lead_IP = document["lead_IP"]
            self.established_connections = document["established_connections"]

        event_info = DatabaseWriter.get_all_documents_in_collection(DatabaseWriter.COLLECTION_EVENT)
        if len(event_info) != 0:
            document = event_info[0]
            self.event_name = document["event_name"]
            self.event_description = document["event_description"]
            self.event_start = document["event_start"]
            self.event_end = document["event_end"]

        directory_info = DatabaseWriter.get_all_documents_in_collection(DatabaseWriter.COLLECTION_DIRECTORY)
        if len(directory_info) != 0:
            document = directory_info[0]
            self.root_directory = document["root_directory"]
            self.red_directory = document["red_directory"]
            self.blue_directory = document["blue_directory"]
            self.white_directory = document["white_directory"]

            self.splunk = SplunkInterface(document["root_directory"], document["red_directory"],
                                          document["blue_directory"], document["white_directory"])
            self.splunk.connect()

        vector_info = DatabaseWriter.get_all_documents_in_collection(DatabaseWriter.COLLECTION_VECTOR)
        print(str(vector_info))
        if len(vector_info) != 0:
            for vector_doc in vector_info:
                retrieved_vector = Vector(vector_doc["name"], vector_doc["description"])

                for log_entry_doc in vector_doc["log_entries"]:
                    retrieved_log = LogEntry(log_entry_doc["_id"], log_entry_doc["data"], log_entry_doc["time"], log_entry_doc["source_index"], log_entry_doc["source_file"], log_entry_doc["source_type"])
                    retrieved_vector.add_log_entry(retrieved_log)
                self.vectors.append(retrieved_vector)

        icon_info = DatabaseWriter.get_all_documents_in_collection(DatabaseWriter.COLLECTION_ICON)
        if len(icon_info) != 0:
            self.icons = [Icon(icon_doc["name"], icon_doc["source"]) for icon_doc in icon_info]

    # Set the team information
    def set_team(self, is_Lead, lead_IP, established_connections):
        self.is_lead = is_Lead
        self.lead_IP = lead_IP
        self.established_connections = established_connections
        DatabaseWriter.write_dict_to_collection(self.get_team_dict(), DatabaseWriter.COLLECTION_TEAM)
        DatabaseWriter.print_collection(DatabaseWriter.COLLECTION_TEAM)

    # Set the event information
    def set_event(self, name, description, start_time, end_time):
        self.event_name = name
        self.event_description = description
        self.event_start = start_time
        self.event_end = end_time
        DatabaseWriter.write_dict_to_collection(self.get_event_dict(), DatabaseWriter.COLLECTION_EVENT)
        DatabaseWriter.print_collection(DatabaseWriter.COLLECTION_EVENT)

    # Set the directory info
    def set_directories(self, root_dir, red_dir, blue_dir, white_dir):
        self.root_directory = root_dir
        self.red_directory = red_dir
        self.blue_directory = blue_dir
        self.white_directory = white_dir

        print("root files")
        self.root_files = self.get_filepaths_from_directory(root_dir)
        print(self.root_files)

        print("red files")
        self.red_files = self.get_filepaths_from_directory(red_dir)
        print(self.red_files)

        print("blue files")
        self.blue_files = self.get_filepaths_from_directory(blue_dir)
        print(self.blue_files)

        print("white files")
        self.white_files = self.get_filepaths_from_directory(white_dir)
        print(self.white_files)

        DatabaseWriter.write_dict_to_collection(self.get_directories_dict(), DatabaseWriter.COLLECTION_DIRECTORY)
        DatabaseWriter.print_collection(DatabaseWriter.COLLECTION_DIRECTORY)

        self.splunk = SplunkInterface(self.root_files, self.red_files, self.blue_files, self.white_files)
        self.splunk.connect()
        Thread(target=self.splunk.start_ingestion).start()

    # Given a directory, get a list of files in the directory as file paths
    def get_filepaths_from_directory(self, dir):
        file_paths = []
        if len(dir) == 0:
            return file_paths
        for path in os.listdir(dir):
            full_path = os.path.join(dir, path)
            if os.path.isfile(full_path):
                file_paths.append(full_path)
        return file_paths

    # Add a vector to configuration. Store in database.
    def add_vector(self, name, description):
        new_vector = Vector(name, description)
        self.vectors.append(new_vector)
        DatabaseWriter.write_dict_to_collection(new_vector.get_dict(), DatabaseWriter.COLLECTION_VECTOR)

    # Delete vector from configuration. Remove from database.
    def delete_vector(self, vectorName):
        for i in range(len(self.vectors)):
            if self.vectors[i].name == vectorName:
                del self.vectors[i]
                DatabaseWriter.delete_one_from_collection({"name": vectorName}, DatabaseWriter.COLLECTION_VECTOR)
                break

    # Add icon to configuration. Add to database.
    def add_icon(self, name, source):
        new_icon = Icon(name, source)
        self.icons.append(new_icon)
        DatabaseWriter.write_dict_to_collection(new_icon.get_dict(), DatabaseWriter.COLLECTION_ICON)

    # Delete Icon from configuration. Delete from Database.
    def delete_icon(self, iconName):
        for i in range(len(self.icons)):
            if self.icons[i].name == iconName:
                del self.icons[i]
                DatabaseWriter.delete_one_from_collection({"name": iconName}, DatabaseWriter.COLLECTION_ICON)
                break

    # Get dictionary representation of team
    def get_team_dict(self):
        return {"is_Lead": self.is_lead,
                "lead_IP": self.lead_IP,
                "established_connections": self.established_connections}

    # Get dictionary representation of event
    def get_event_dict(self):
        return {"event_name": self.event_name,
                "event_description": self.event_description,
                "event_start": self.event_start,
                "event_end": self.event_end}

    # Get dictionary representation of directories
    def get_directories_dict(self):
        return {"root_directory": self.root_directory,
                "red_directory": self.red_directory,
                "blue_directory": self.blue_directory,
                "white_directory": self.white_directory}

    # Get dictionary representation of vectors
    def get_list_of_vector_dicts(self):
        return [vector.get_dict() for vector in self.vectors]

    # Get dictionary representation of icons
    def get_list_of_icon_dicts(self):
        return [icon.get_dict() for icon in self.icons]
