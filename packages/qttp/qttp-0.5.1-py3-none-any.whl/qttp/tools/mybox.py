import dropbox
import pandas as pd

class Dropbox:
    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token)

    def get_file_list_names(self, path):
        contents = self.dbx.files_list_folder(path)
        files_name = [content.name for content in contents.entries]
        return files_name

    def just_read_csv(self, path):
        downfile, f = self.dbx.files_download(path)
        df = pd.read_csv(f.raw)
        return df

    def read_csv(self, path):
        downfile, f = self.dbx.files_download(path)
        df = pd.read_csv(f.raw, index_col=['date'])
        df.index = pd.to_datetime(df.index)
        return df

    def create_file(self, path, dataframe):
        df_string = dataframe.to_csv()
        db_bytes = bytes(df_string, 'utf8')
        self.dbx.files_upload(
            f=db_bytes,
            path=path,
            mode=dropbox.files.WriteMode.overwrite
        )

# token = 'lIgpKvzLKUoAAAAAAAAAAa4xVvjumDPWWL6Gz3k6nUlKB3l8ArY3TsDHuAPNhQm4'
# box = Dropbox(token)
#
# file_path = '/other/'
# file_name = f'moon_phase_with_no_emoji.csv'
#
# print(box.read_csv(file_path + file_name).index)
