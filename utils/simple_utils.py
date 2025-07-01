import os, shutil

def list_filenames(directory):
    try:
        # 获取文件夹中的所有文件名
        filenames = [f for f in os.listdir(directory) if f not in ('.', '..')]
        return filenames
    except Exception as e:
        return []

def load_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise Exception(f"<script system>: file: {os.path.basename(file_path)} not found")