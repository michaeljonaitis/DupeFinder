import hashlib
import os
import sys

from datetime import datetime

class DupeFinderError(Exception):
    pass

class DupeFinder():
    def __init__(self, target_dir):
        self.should_buffer = 1
        self.target_dir = str(target_dir)

    @staticmethod
    def get_hash(path, buffer_size):
        hasher = hashlib.md5()
        the_file = open(path, 'rb')
        buff = the_file.read(buffer_size)
        while buff:
            hasher.update(buff)
            buff = the_file.read(buffer_size)
        return hasher.hexdigest()

    def find_duplicates(self):
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

        print("--- Duplicate Files ---")
        for duplicate_file in duplicates:		
            print(duplicates.get(duplicate_file))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
        if os.path.exists(target_dir):
            startTime = datetime.now()
            DupeFinder(target_dir).find_duplicates()
            print("{} - {}".format('Time Elapsed:', datetime.now() - startTime))
        else:
            raise DupeFinderError("Folder not found.")
            
    elif len(sys.argv) == 0:
        raise DupeFinderError("Folder argument required eg. $ python deduper.py '<path to file>'.")

    elif len(sys.argv) > 2:
        raise DupeFinderError("Can dedupe only one folder at a time.")







