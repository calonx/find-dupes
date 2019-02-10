
import hashlib
import os
import sys
from tqdm import tqdm

s_TargetPath = os.path.split(os.getcwd())[0]

s_Files = []

#---------------------------------------------------------------------------------------------------
def CountItems(file_path):
    if not os.path.exists(file_path):
        return 0
    count = 1
    if os.path.isdir(file_path):
        for entry in os.scandir(file_path):
            count += CountItems(entry.path)
    return count
        


#---------------------------------------------------------------------------------------------------
def ProcessItem(file_path, callback=lambda path, digest: print(f'{digest} {path}')):
    if not os.path.exists(file_path):
        return None

    m = hashlib.sha256()
    if os.path.isdir(file_path):
        for entry in os.scandir(file_path):
            item_hash = ProcessItem(entry.path, callback)
            m.update(item_hash)
    else:
        with open(file_path, 'rb') as f:
            m.update(f.read())
    
    callback(file_path, m.hexdigest())
    return m.digest()

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('No path(s) provided.')
        exit(1)

    with open('results.log', 'w') as f:
        for path in sys.argv[1:]:
            count = CountItems(path)
            print(f'{count} {path}')
            with tqdm(total=count, unit='files') as progress:
                def callback(path, digest):
                    progress.update(1)
                ProcessItem(path, callback)
