import argparse
import os
from collections import defaultdict


def get_parse_argv():
    parse = argparse.ArgumentParser(
        description='Find duplicate files'
    )
    parse.add_argument(
        '--directory',
        '-d',
        help='path to root directory'
    )
    return parse.parse_args()


def get_full_files_path(root_dir_path):
    all_file_paths = defaultdict(list)
    for root, dirs, files in os.walk(root_dir_path):
        for file in files:
            try:
                full_file_path = os.path.join(root, file)
                size_file = os.path.getsize(full_file_path)
            except (UnicodeEncodeError, FileNotFoundError):
                print ('Не могу прочитать {}'.format(file))
                continue
            all_file_paths[(file, size_file)].append(full_file_path)
    return all_file_paths


def get_dublicate_files(all_file_paths):
    dublicate_files = {}
    for file in all_file_paths:
        if len(all_file_paths[file]) > 1:
            dublicate_files.update({file: all_file_paths[file]})
    return dublicate_files


def print_dublicate_files(dublicate_files):
    print('Найдены файлы с одинаковым именем и размером:')
    for file_name, file_size in dublicate_files:
        print('{} ({} байт):'.format(file_name, file_size))
        [print("\t\t{}".format(file_path)) for file_path in dublicate_files[(file_name, file_size)]]


if __name__ == '__main__':
    pass
    root_dir_path = get_parse_argv().directory
    if os.path.isdir(root_dir_path):
        all_file_paths = get_full_files_path(root_dir_path)
        dublicate_files = get_dublicate_files(all_file_paths)
        if dublicate_files:
            print_dublicate_files(dublicate_files)
        else:
            print('Повторяющихся файлов не обнаружено')
    else:
        print('Неверное имя директории. ВВедите верное имя')
