import os
import sys
from multiprocessing import Pool
import subprocess


class GitUploadProjects:
    def __init__(self, __args=sys.argv, __dir_path=os.path.dirname(os.path.realpath(__file__))):
        self.__dir_path = __dir_path
        # self.__dir_path = "/Users/qin/qinProject/Unity3DAsset"
        self.__folder_list = os.listdir(self.__dir_path)
        self.__repositories_list_name = "repositories.txt"
        self.__git_url = "ssh://unityassets@cq.qinyupeng.com:10022/GitRepositories/unityassets"
        self._list_repositories()
        self.__ignore_folder_list = [".git", ".vscode"]
        self.__ignore_file_list = [".DS_Store"]
        self.__folder_name = ""
        self.__analysis_folder_name(__args)

    def __get_all_folders(self):
        folder_list = []
        for folder_name in os.listdir(self.__dir_path):
            if os.path.isdir(self.__dir_path+'/'+folder_name):
                folder_list.append(folder_name)
        folder_list.sort()
        return folder_list

    def _add_remote_repositories(self):
        folder_list = self.__get_all_folders()
        for folder_name in folder_list:
            if os.path.isdir(self.__dir_path+'/'+folder_name):
                os.chdir(self.__dir_path+'/'+folder_name)
                print(f"--------------------{folder_name}------------------------")
                os.system(f"git init")
                os.system(f"git remote remove remote")
                os.system(f"git remote add remote {self.__git_url}/"+folder_name+".git")
                print(f"")
                os.chdir(self.__dir_path)

    def _commit_push_repositories(self):
        folder_list = self.__get_all_folders()
        for folder_name in folder_list:
            self._upload_thread(folder_name)

        # with Pool() as p:
        #     p.map(self._upload_thread, [folder_name for folder_name in folder_list])

    def _upload_thread(self, folder_name):
        if os.path.isdir(self.__dir_path+'/'+folder_name):
            os.chdir(self.__dir_path+'/'+folder_name)
            print(f"--------------------{folder_name}------------------------")
            output = subprocess.getoutput("git status")
            if ("nothing to commit" in output):
                print("nothing to commit")
                print(f"")
                return
            print("start commit:"+folder_name)
            self.__start_upload(self.__dir_path+'/'+folder_name)
            print(f"")
            os.chdir(self.__dir_path)

    def _push_repositories(self):
        folder_list = self.__get_all_folders()
        for folder_name in folder_list:
            if os.path.isdir(self.__dir_path+'/'+folder_name):
                os.chdir(self.__dir_path+'/'+folder_name)
                print(f"--------------------{folder_name}------------------------")
                os.system("git push --set-upstream remote master")
                print(f"")
                os.chdir(self.__dir_path)

    def _create_repositories_record_file(self):
        if os.path.exists(f"{self.__dir_path}/{self.__repositories_list_name}"):
            os.remove(f"{self.__dir_path}/{self.__repositories_list_name}")
        with open(f"{self.__dir_path}/{self.__repositories_list_name}", "w+") as f:
            f.seek(0)
            for folder_name in self.__get_all_folders():
                if os.path.isdir(self.__dir_path+'/'+folder_name):
                    f.write(str(folder_name)+"\n")

    def _git_list(self):
        repositories_list = []
        exist_repositories_list = []
        with open(f"{self.__dir_path}/repositories_list.txt", "r") as f:
            repositories_list = f.readlines()
        exist_repositories_list = os.listdir(self.__dir_path)
        for folder_name in exist_repositories_list:
            if folder_name.find(".") != -1:
                exist_repositories_list.remove(folder_name)
        new_repositories_list = list(
            set(repositories_list+exist_repositories_list))
        print(str(new_repositories_list))
        with open(f"{self.__dir_path}/repositories_list.txt", "w+") as f:
            f.seek(0)
            for line in new_repositories_list:
                if line != "\n" and line != "repositories_list.txt":
                    f.write(str(line))

    def _pull(self):
        with open(f"{self.__dir_path}/{self.__repositories_list_name}") as f:
            repositories_list = f.readlines()
        # folder_list = os.listdir(repositories_list)
        for repositories in repositories_list:
            repositories = repositories.replace("\n", "")
            # os.chdir(self.__dir_path+'/'+folder_name)
            print(f"[_pull]pulling[{repositories}]")
            # os.system("git init")
            os.system(f"git clone {self.__git_url}" + repositories+".git")
            # os.system("git add .")
            # os.system("git commit -m \"new update\"")
            # os.system("git push git")
            # os.chdir(self.__dir_path)
            print("[_pull]Updated repositories:"+repositories)

    def _list_repositories(self):
        folder_list = []
        if os.path.isfile(f"{self.__dir_path}/{self.__repositories_list_name}"):
            with open(f"{self.__dir_path}/{self.__repositories_list_name}", "r") as f:
                folder_list = f.readlines()
        with open(f"{self.__dir_path}/{self.__repositories_list_name}", "a") as f:
            for folder_name in os.listdir(self.__dir_path):
                if os.path.isdir(self.__dir_path+'/'+folder_name):
                    if folder_name+"\n" not in folder_list:
                        f.write(folder_name+"\n")

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

    def __upload_part(self, folder_path, __file_list):
        os.chdir(folder_path)
        _add_list = []
        for file_name in __file_list:
            os.system(f"git add -f '{file_name}'")
            _add_list.append(file_name)
        output = ""
        while(True):
            os.system(f'git commit -m "update\n{self.__string_builder_list(_add_list)}"')
            output = subprocess.getoutput("git push --set-upstream remote master")
            print(output)
            if "Everything up-to-date" in output:
                break


    def __start_upload(self, folder_path):
        _files_ = self.__list_repositories(folder_path)
        bash_list = self.__get_files_batch(_files_)
        for index, _list in enumerate(bash_list):
            self.__upload_part(folder_path, _list)
            print(f"batch {index+1} of {len(bash_list)} uploaded")

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


if __name__ == '__main__':
    gm = GitUploadProjects()
    gm._create_repositories_record_file()
    gm._add_remote_repositories()
    gm._commit_push_repositories()
    # gm._upload_thread("Art2D_ICON")
