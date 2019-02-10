
import hashlib
import os
import sys
import multiprocessing as mp
from tqdm import tqdm

s_TargetPath = os.path.split(os.getcwd())[0]

s_Files = []

#---------------------------------------------------------------------------------------------------
def CountItems(file_path, callback=None):
    if not os.path.exists(file_path):
        return 0
    count = 1
    if callback:
        callback(file_path)
    if os.path.isdir(file_path):
        for entry in os.scandir(file_path):
            count += CountItems(entry.path, callback)
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
def ProcessTree(path):
    print(f'Processing {path}...')

    with tqdm('Counting', unit=' files') as prog:
        count = CountItems(path, lambda p: prog.update(1))

    # with tqdm('Hashing', total=count, unit=' files') as progress:
    #     def callback(path, digest):
    #         progress.update(1)

    #     ProcessItem(path, callback)

#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('No path(s) provided.')
        exit(1)

    processes = [mp.Process(target=ProcessTree, args=[path]) for path in sys.argv[1:]]

    for proc in processes:
        proc.start()
    
    for proc in processes:
        proc.join()
    
    print('All done!')