import os
import sys
from datetime import datetime

from dupefinder import DupeFinder, DupeFinderError


if __name__ == '__main__':
    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
        if os.path.exists(target_dir):
            startTime = datetime.now()
            dupe_finder = DupeFinder(target_dir)
            duplicates = dupe_finder.find_duplicates()
            print("{} - {}".format('Time Elapsed:', datetime.now() - startTime))
            dupe_finder.print_results(duplicates)
        else:
            raise DupeFinderError("Folder not found.")
            
    elif len(sys.argv) == 0:
        raise DupeFinderError("Folder argument required eg. $ python deduper.py '<path to file>'.")

    elif len(sys.argv) > 2:
        raise DupeFinderError("Can dedupe only one folder at a time.")

