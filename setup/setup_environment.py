import os
import shutil


class Setup:
    def __init__(self) -> None:
        current_directory = os.getcwd()
        self.tmp_workdir = f"{current_directory}/tmp"
        self.download_folder = None

    def init(self):
        self.__create_tmp_dir()
        self.__create_download_folder()
        os.environ["DOWNLOAD_FOLDER"] = self.download_folder
        os.environ["TMP_WORKDIR"] = self.tmp_workdir

    def finalize(self):
        self.__clear_tmp_dir()

    def __create_tmp_dir(self):
        try:
            os.mkdir(self.tmp_workdir)
        except FileExistsError:
            pass

    def __create_download_folder(self):
        download_folder = f"{self.tmp_workdir}/download"
        try:
            os.mkdir(download_folder)
            self.download_folder = download_folder
        except FileExistsError:
            self.download_folder = download_folder

    def __clear_tmp_dir(self):

        shutil.rmtree(self.tmp_workdir)
