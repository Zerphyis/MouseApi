import os
import time


class FileManager:
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_upload(self, filename, file_bytes):
        safe_name = os.path.basename(filename)
        path = os.path.join(self.upload_dir, f"{int(time.time())}_{safe_name}")
        with open(path, 'wb') as f:
            f.write(file_bytes)
        return path

    def list_files(self):
        return os.listdir(self.upload_dir)

    def get_path(self, name):
        candidate = os.path.join(self.upload_dir, name)
        if not os.path.exists(candidate):
            raise FileNotFoundError(name)
        return candidate
