class DataStructure:
    def __init__(self, origin_string_data, clean_string_data, placeholder, source_file = None):
        self.origin_string_data = origin_string_data
        self.clean_string_data = clean_string_data
        self.placeholder = set(placeholder)
        self.source_file = source_file

    def __repr__(self):
        return f"DataStructure(origin_string_data={self.origin_string_data}, clean_string_data={self.clean_string_data}, placeholder={self.placeholder}, source_file={self.source_file})"