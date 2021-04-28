#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
function: This script resolves locales's BEP inconsistence,
          it scans a specific path and replaces the same file 
          in that path with a hard link.Avoid different language 
          packs each time due to concurrent compilation.
"""
import os
import sys
import time

all_file = {}

def cmp_file(f1, f2):
    """compare two files in bytes"""
    st1 = os.stat(f1)
    st2 = os.stat(f2)

    bufsize = 8 * 1024
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True


def search_all_inode(dir_path):
    """recursively traverse the directory to group all"""
    files = os.listdir(dir_path)
    
    for fi in files:
        fi_d = os.path.join(dir_path, fi)
        if os.path.isdir(fi_d):
            search_all_inode(fi_d)
        else:
            size = os.stat(fi_d).st_size
            if size in all_file:
                all_file[size].append(fi_d)
            else:
                all_file[size] = [fi_d]


def deal_one(file_paths):
    """traverse the file array, delete the same file and create a hard link"""
    file_count = len(file_paths)
    inode_files = {}

    for i in range(0, file_count):
        for j in range(i + 1, file_count):
            file1 = file_paths[i]
            file2 = file_paths[j]
            
            file1_inode = os.stat(file1).st_ino
            file2_inode = os.stat(file2).st_ino

            if file1_inode not in inode_files:
                inode_files[file1_inode] = file1
                
            if file1_inode == file2_inode:
                continue

            if cmp_file(file1, file2):
                print('deal same file：', file1, '==', file2)
                os.remove(file2)
                os.link(file1, file2)
            else:
                if file2_inode not in inode_files:
                    inode_files[file2_inode] = file2


def deal_files():
    """get file array and processed one by one"""
    for size in all_file:
        file_paths = all_file[size]
        if len(file_paths) > 1:
            deal_one(file_paths)


def usage():
    """print usage"""
    print("""
rm_same_file: Replace the same file with a hard link.

rm_same_file.py [target path]

    """)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        search_all_inode(sys.argv[1])
        deal_files()
    else:
        usage()
        sys.exit()
