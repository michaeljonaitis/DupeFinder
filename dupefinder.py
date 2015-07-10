import hashlib
import os

class DupeFinderError(Exception):
    pass

class DupeFinder():
    def __init__(self, target_dir):
        """
        Assign instance variables during construction.
        """
        self.should_buffer = 1
        self.target_dir = str(target_dir)

    @staticmethod
    def print_results(duplicates):
        """
        Loop through results and pretty print.
        """
        print("--- Found {} Duplicate Files ---".format(len(duplicates)))
        for duplicate_file in duplicates:		
            print(duplicates.get(duplicate_file))

    @staticmethod
    def get_hash(path, buffer_size):
        """
        Generates a hash of the file block by block to
        avoid issues when hasing large files.
        """
        hasher = hashlib.sha256()
        the_file = open(path, 'rb')
        file_buffer = the_file.read(buffer_size)
        while file_buffer:
            hasher.update(file_buffer)
            file_buffer = the_file.read(buffer_size)
        return hasher.hexdigest()

    def find_duplicates(self):
        """
        Walk the target directory, follow all simlinks, and perform hash comparisons
        to determine if any files are duplicates.  

        Tried to improve this by comparing file sizes before hashing in the file_size_version
        branch.  Ran into large performance issues using this technique... next move was to 
        profile the script to find bottleneck
        """
        unique_files = dict()
        duplicates = dict()
        for dir_name, sub_dir_names, all_files in os.walk(self.target_dir, followlinks=True):
            for a_file in all_files:
                file_path = '{}/{}'.format(dir_name, a_file)
                file_hash = self.get_hash(file_path, self.should_buffer)
                if file_hash in unique_files:
                    duplicates.update({file_hash:file_path})
                else:
                    unique_files.update({file_hash:file_path})
        return duplicates



