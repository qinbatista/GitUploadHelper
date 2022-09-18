import os
import sys


class GitUploadHelper:
    def __init__(self, __args):
        self.__ignore_folder_list = [".git", ".vscode"]
        self.__ignore_file_list = [".DS_Store"]
        self.__folder_name = ""
        self.__analysis_folder_name(__args)

    def __list_repositories(self, _path):
        _folder_list = []
        for dirpath, dirnames, filenames in os.walk(_path):
            if self.__is_contain_the_key_in_ignore_folder_list(dirpath) == False:
                for filename in filenames:
                    if self.__is_contain_the_key_in_ignore_file_list(filename) == False:
                        _folder_list.append(os.path.join(dirpath, filename))
        return _folder_list

    def __is_contain_the_key_in_ignore_folder_list(self, key):
        for list_name in self.__ignore_folder_list:
            if list_name in key:
                return True
        return False

    def __is_contain_the_key_in_ignore_file_list(self, key):
        for list_name in self.__ignore_file_list:
            if list_name in key:
                return True
        return False

    def __analysis_folder_name(self, __args):
        if __args.__len__() >= 2:
            self.__folder_name = __args[1]
        else:
            self.__folder_name = os.path.dirname(__file__)

    def __upload_part(self, __file_list):
        os.chdir(self.__folder_name)
        _add_list = []
        for file_name in __file_list:
            os.system(f"git add '{file_name}'")
            _add_list.append(file_name)
        os.system(f'git commit -m "update\n{self.__string_builder_list(_add_list)}"')
        os.system("git push")

    def _start(self):
        _files_ = self.__list_repositories(self.__folder_name)
        bash_list = self.__get_files_batch(_files_)
        for index, _list in enumerate(bash_list):
            self.__upload_part(_list)
            print(f"batch {index+1} of {len(bash_list)} uploaded")
        os.system("git add -A && git commit -m \"final\"")

    def __string_builder_list(self, _list):
        _string = ""
        for _string_ in _list:
            _string += _string_ + "\n"
        return _string

    def __get_files_batch(self, _list):
        _batch_ = []
        _batch_list = []
        _size = 0
        for _string_ in _list:
            if _size < 1024 * 1024 * 10:
                _size += os.path.getsize(_string_)
                _batch_list.append(_string_)
            else:
                _new_list = _batch_list.copy()
                _batch_.append(_new_list)
                _batch_list.clear()
                _size = 0
        return _batch_


if __name__ == "__main__":
    git_upload_helper = GitUploadHelper(sys.argv)
    git_upload_helper._start()
