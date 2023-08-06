# -*- coding: UTF-8 -*-
import json
import os
import pickle
import zipfile
from pathlib import Path


class FileProcessing:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all_data(self):
        """
        一次读取整个文件
        :return: <class 'str'>
        """
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            return f.read()

    def read_file_by_line(self):
        """
        按行读取，去掉行尾换行符
        :return:
        """
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            while True:
                one_line = f.readline()
                if not one_line:
                    return
                else:
                    yield one_line.strip()

    def write_file_all(self, data_list):
        """
        写入数据到文件
        :param data_list:
        :return:
        """
        with open(self.file_path, 'a', encoding='utf-8') as f:
            for line in data_list:
                f.write(str(line) + '\n')

    def check_file_exist(self):
        """
        检查文件是否存在
        :return:
        """
        return os.path.exists(self.file_path)

    def get_file_data_len(self):
        """
        获取文件总行数
        :return:
        """
        i = 0
        for i, _ in enumerate(self.read_file_by_line()):
            i += 1
        return i

    def get_file_dir(self):
        """
        获取文件所在目录
        :return:
        """
        return Path(self.file_path).resolve().parent

    def get_file_size(self):
        """
        获取文件大小
        :return:
        """
        file_size = os.path.getsize(self.file_path) / 1024
        size_unit = "KB"

        if file_size > 1024:
            file_size = file_size / 1024
            size_unit = "MB"

        return f"{file_size:.3f} {size_unit}"


def check_file_contents(f1, f2, check=False):
    """
    比较两个文件内容是否一致
    :param check: 是否详细对比（按照字节对比，效率低下，默认为False）两个文件
    :param f1: 文件一
    :param f2: 文件二
    :return:
    """
    st1 = os.stat(f1)
    st2 = os.stat(f2)

    if check:
        if st1.st_size != st2.st_size:
            return False

        buf_size = 8 * 1024
        with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
            while True:
                b1 = fp1.read(buf_size)  # 读取指定大小的数据进行比较
                b2 = fp2.read(buf_size)
                if b1 != b2:
                    return False
                if not b1:
                    return True
    else:
        if st1.st_size != st2.st_size:
            return False
        else:
            return True


def print_file_directory_tree(current_path, count=0):
    """
    打印文件目录树
    :param current_path:
    :param count:
    :return:
    """
    if not os.path.exists(current_path):
        return
    if os.path.isfile(current_path):
        file_name = os.path.basename(current_path)
        print('\t' * count + '├── ' + file_name)
    elif os.path.isdir(current_path):
        print('\t' * count + '├── ' + current_path)
        path_list = os.listdir(current_path)
        for eachPath in path_list:
            print_file_directory_tree(current_path + '/' + eachPath, count + 1)


def unzip_file(zip_name, target_dir):
    """
    zip文件解压
    :param zip_name: 待解压的zip包名称
    :param target_dir: 解压路径
    :return:
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    file_zip = zipfile.ZipFile(zip_name, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, target_dir)
    file_zip.close()


def save_pickle(data, file_path):
    """
    保存成pickle文件
    :param data:
    :param file_path:
    :return:
    """
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(input_file):
    """
    读取pickle文件
    :param input_file:
    :return:
    """
    with open(input_file, 'rb') as f:
        data = pickle.load(f)
    return data


def save_json(data, file_path, ensure_ascii=False, indent=4):
    """
    保存成json文件
    :param data:
    :param file_path:
    :param ensure_ascii:
    :param indent:
    :return:
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)


def load_json(file_path):
    """
    加载json文件
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
