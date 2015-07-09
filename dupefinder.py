import hashlib
import os

class DupeFinderError(Exception):
    pass

class DupeFinder():
    def __init__(self, target_dir):
        self.should_buffer = 1
        self.target_dir = str(target_dir)

    @staticmethod
    def print_results(duplicates):
        print("--- Found {} Duplicate Files ---".format(len(duplicates)))
        for duplicate_file in duplicates:		
            print(duplicates.get(duplicate_file))

    @staticmethod
    def get_hash(path, buffer_size):
        hasher = hashlib.md5()
        the_file = open(path, 'r')
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
                file_size = os.path.getsize(file_path)

                if unique_files.get(file_size):
                    file_hash = self.get_hash(file_path, self.should_buffer)
                    same_size_files = unique_files.get(file_size)
                    for same_size_file_path in same_size_files:
                        if self.get_hash(same_size_file_path, self.should_buffer) == file_hash:
                            duplicates.update({file_path:file_size})
                        else:
                            unique_files.get(file_size).append(file_path)
                else:
                    unique_files.update({file_size:list([file_path,])})
                
        print('------Duplicate Files------')
        for size, u_file in duplicates.items():
            print("{}-{}bytes".format(size, u_file))

        return duplicates



