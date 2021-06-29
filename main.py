import os
import xxhash
import sqlite3
import time
from multiprocessing import Pool, TimeoutError
import sqlite3


chunksize = 1000000000

# walkpath = r"C:\Users\chris\OneDrive\Desktop\test"

walkpath = "C:\Program Files (x86)\Call of Duty Black Ops Cold War"


start_time = time.time()



con = sqlite3.connect('hashes.db', check_same_thread=False)

filelist = []


def hashFile(file):
    print(file + " being read")
    x = xxhash.xxh3_64() 
    with open(file, 'rb') as f:
        while True:
            read_data = f.read(chunksize)
            if not read_data:
                break # done
            x.update(read_data)  
    return [file, x.hexdigest()]





def main():
    pool = Pool(8) 

    for root, subdirs, files in os.walk(walkpath):
        for name in files:
            filelist.append(os.path.join(root, name))

    hashes = pool.map(hashFile, filelist)

    cur = con.cursor()

    for hash in hashes:
        cur.execute("INSERT INTO hashes VALUES (?, ?)", (hash[0], hash[1]))

    con.commit()
    con.close()

    print("--- %s seconds ---" % (time.time() - start_time))
        
        




if __name__ == '__main__':
  
    main()
    
