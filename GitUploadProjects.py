#
import os
import sys
import time
import json
import threading


class GitUploadProjects:
    def __init__(self, __dir_path=os.path.dirname(os.path.realpath(__file__))):
        self.__dir_path = __dir_path
        # self.__dir_path = "/Users/qin/qinProject/Unity3DAsset"
        self.__folder_list = os.listdir(self.__dir_path)
        self.__repositories_list_name = "repositories.txt"
        self.__git_url = "ssh://unityassets@cq.qinyupeng.com:10022/GitRepositories/unityassets"
        self._list_repositories()

    def _push(self):
        for folder_name in self.__folder_list:
            if os.path.isdir(self.__dir_path+'/'+folder_name):
                os.chdir(self.__dir_path+'/'+folder_name)
                print(f"Project:{'['+folder_name}]")
                os.system("pwd")
                os.system("git init")
                os.system(f"git remote add remote {self.__git_url}/"+folder_name+".git")
                os.system("git add .")
                os.system("git commit -m \"new update\"")
                os.system("git push --set-upstream remote master")
                os.chdir(self.__dir_path)
                os.system("pwd")

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

    def _commit_repositories(self):
        folder_list = self.__get_all_folders()
        for folder_name in folder_list:
            if os.path.isdir(self.__dir_path+'/'+folder_name):
                os.chdir(self.__dir_path+'/'+folder_name)
                print(f"--------------------{folder_name}------------------------")
                os.system("git add .")
                os.system("git commit -m \"new update\"")
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

    def _commit_and_push_repositories(self):
        self._commit_repositories()
        self._push_repositories()

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


if __name__ == '__main__':
    gm = GitUploadProjects()
    gm._create_repositories_record_file()
    gm._add_remote_repositories()
    gm._commit_repositories()
    gm._push_repositories()

