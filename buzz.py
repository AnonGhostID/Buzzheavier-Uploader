import sys
import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Semaphore

def clean_filename(filename):
    return filename.replace(' ', '').replace('-', '')

class ProgressFile:
    def __init__(self, filename, filesize, bar):
        self.file = open(filename, 'rb')
        self.filesize = filesize
        self.bar = bar
        self.lock = Lock()

    def read(self, size):
        with self.lock:
            data = self.file.read(size)
            if not data:
                self.bar.close()
                return b''
            self.bar.update(len(data))
            return data

    def __len__(self):
        return self.filesize

    def close(self):
        self.file.close()

def upload_file(file_path, position, semaphore):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}", file=sys.stderr)
        return None

    basename = os.path.basename(file_path)
    stripped_basename = clean_filename(basename)
    url = f"https://w.buzzheavier.com/{stripped_basename}"
    filesize = os.path.getsize(file_path)

    with semaphore:
        with tqdm(
            total=filesize,
            unit='B',
            unit_scale=True,
            desc=basename,
            position=position,
            leave=True,
            dynamic_ncols=True
        ) as bar:
            pf = ProgressFile(file_path, filesize, bar)
            headers = {'Content-Length': str(filesize)}
            try:
                response = requests.put(url, data=pf, headers=headers)
                pf.close()
                try:
                    data = response.json()
                    return data["data"]["id"]
                except Exception:
                    print(f"UPLOAD FAILED or unexpected server response for {file_path}", file=sys.stderr)
                    return None
            except Exception as e:
                pf.close()
                print(f'Upload failed for {file_path}:', e, file=sys.stderr)
                return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file1> [file2 ...]")
        sys.exit(1)

    files = sys.argv[1:]
    links = [None] * len(files)
    max_workers = 4

    semaphore = Semaphore(max_workers)

    def upload_with_position(args):
        file_path, idx = args
        position = idx % max_workers
        return idx, upload_file(file_path, position, semaphore)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(upload_with_position, (file, idx)) for idx, file in enumerate(files)]
        for future in as_completed(futures):
            idx, file_id = future.result()
            if file_id:
                links[idx] = f"https://buzzheavier.com/{file_id}"

    final_links = [link for link in links if link]
    if final_links:
        with open("links.txt", "w") as f:
            for link in final_links:
                f.write(link + "\n")
