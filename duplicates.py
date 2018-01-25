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
        help='path to root directory',
        type=str
    )
    return parse.parse_args()


def get_full_files_path(root_dir_path):
    all_file_paths = defaultdict(list)
    for root, dir_name, file_names in os.walk(root_dir_path):
        for file_name in file_names:
            full_file_path = os.path.join(root, file_name)
            size_file = os.path.getsize(full_file_path)
            all_file_paths[(file_name, size_file)].append(full_file_path)
    return all_file_paths


def get_dublicate_files(all_file_paths):
    dublicate_files = {}
    for file_names in all_file_paths:
        if len(all_file_paths[file_names]) > 1:
            dublicate_files.update({file_names: all_file_paths[file_names]})
    return dublicate_files


def print_dublicate_files(dublicate_files):
    print('Найдены файлы с одинаковым именем и размером:')
    for file_name, file_paths in dublicate_files.items():
        print('{} ({} байт):'.format(*file_name))
        [print("\t\t{}".format(file_path)) for file_path in file_paths]


if __name__ == '__main__':
    root_dir_path = get_parse_argv().directory
    if os.path.isdir(root_dir_path):
        all_file_paths = get_full_files_path(root_dir_path)
        dublicate_files = get_dublicate_files(all_file_paths)
        if dublicate_files:
            print_dublicate_files(dublicate_files)
        else:
            print('Повторяющихся файлов не обнаружено')
    else:
        print('Неверное имя директории. Введите верное имя')
