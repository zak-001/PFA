import os
import difflib

def get_all_files(directory):
    """
    Returns a dict mapping relative paths to full paths for all files under 'directory'
    """
    file_map = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)
            file_map[rel_path] = full_path
    return file_map

def compare_files(file1, file2):
    with open(file1, 'r', errors='ignore') as f1, open(file2, 'r', errors='ignore') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    diff = list(difflib.unified_diff(
        f1_lines, f2_lines,
        fromfile=file1,
        tofile=file2,
        lineterm=''
    ))

    if diff:
        print(f"\n[DIFFERENCES in {os.path.basename(file1)} ({os.path.relpath(file1)})]")
        for line in diff:
            print(line)
    else:
        print(f"[MATCH] {os.path.relpath(file1)}")

def compare_directories_recursive(dir1, dir2):
    files1 = get_all_files(dir1)
    files2 = get_all_files(dir2)

    all_keys = set(files1.keys()).union(files2.keys())

    for key in sorted(all_keys):
        path1 = files1.get(key)
        path2 = files2.get(key)

        if not path1:
            print(f"[ONLY IN {dir2}] {key}")
        elif not path2:
            print(f"[ONLY IN {dir1}] {key}")
        else:
            compare_files(path1, path2)

# Example usage:
compare_directories_recursive('/path/to/dir1', '/path/to/dir2')
