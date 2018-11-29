import argparse
import configparser
from pathlib import Path

import dropbox


class DropboxHandler:

    def __init__(self, apikey):
        self.dbx = dropbox.Dropbox(apikey, timeout=30)
        self.CHUNK_SIZE = 4 * 1024 * 1024
        self.DEFAULT_LOCAL_PATH = "C:\\Downloads\\"
        self.DEFAULT_REMOTE_PATH = "/"

    # Dropbox download
    def download_file(self, remote_path, local_path):
        if not remote_path:
            raise Exception("Download source is missing")
        filename = remote_path.split("/")[-1]
        print(f"Getting {filename} from Dropbox...")
        dest_file = local_path or self.DEFAULT_LOCAL_PATH + filename

        try:
            self.dbx.files_download_to_file(dest_file, remote_path)
        except dropbox.exceptions.ApiError:
            print("Error: file cannot be found!")
            return
        print("File has finished downloading to", dest_file)

        print("Removing from cloud...")
        try:
            self.dbx.files_delete_v2(remote_path)
        except dropbox.exceptions.ApiError:
            print("Error: file cannot be deleted!")
            return
        print("Done")

    def upload_file(self, local_path, remote_path):
        """
        Uploads a file to Dropbox and returns the temporary (24 hours) link
        """

        if not local_path:
            raise Exception("Upload source is missing")

        # Process file
        file_name = local_path.split("\\")[-1]
        dest_path = remote_path or self.DEFAULT_REMOTE_PATH + file_name

        read_file = open(local_path, 'rb')
        print()
        file_size = Path(local_path).stat().st_size
        file_size_megs = "{0:.2f} KB".format(file_size/1024)

        # Upload file
        print(f"Uploading {file_name} ({file_size_megs})")
        if file_size <= self.CHUNK_SIZE:
            self.dbx.files_upload(
                read_file.read(),
                dest_path,
                mute=True
            )
            print("Done")
        else:
            upload_session_start_result = self.dbx.files_upload_session_start(
                read_file.read(self.CHUNK_SIZE)
            )
            cursor = dropbox.files.UploadSessionCursor(
                session_id=upload_session_start_result.session_id,
                offset=read_file.tell()
            )
            commit = dropbox.files.CommitInfo(path=dest_path)

            # Upload in chunks and show status bar
            toolbar_width = 30

            while read_file.tell() < file_size:
                if ((file_size - read_file.tell()) <= self.CHUNK_SIZE):
                    self.dbx.files_upload_session_finish(
                        read_file.read(self.CHUNK_SIZE),
                        cursor, commit
                    )
                else:
                    self.dbx.files_upload_session_append(
                        read_file.read(self.CHUNK_SIZE),
                        cursor.session_id, cursor.offset
                    )
                    cursor.offset = read_file.tell()
                    progress = cursor.offset/file_size
                    bars = int(toolbar_width*progress)
                    print(
                        f"{'█' * bars}{'░' * (toolbar_width - bars)} "
                        f"{int(progress*100)}%",
                        end="\r"
                    )
            print(f"Done{' ' * (toolbar_width)}", end="\r")

        return self.dbx.files_get_temporary_link(dest_path)


def get_api_key():
    if args.api_key:
        return args.api_key
    else:
        config = configparser.ConfigParser()
        config.read('settings.ini')
        return config.get('APIkeys', 'Dropbox')
    raise


# Parse command line arguments if running standalone
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
        Dropbox handler: a wrapper for the Dropbox API
        """
    )
    parser.add_argument(
        "operation",
        help="either 'upload' or 'download'"
    )
    parser.add_argument(
        "-l",
        "--local",
        help="the path of the local file"
    )
    parser.add_argument(
        "-r",
        "--remote",
        help="the path of the remote file"
    )
    parser.add_argument(
        "-k",
        "--api_key",
        help="the API key to your Dropbox app"
    )
    args = parser.parse_args()

    dbh = DropboxHandler(get_api_key())
    valid_commands = {
        "upload": dbh.upload_file,
        "download": dbh.download_file,
    }

    if args.operation not in valid_commands:
        print("Missing or invalid operation")
    else:
        valid_commands[args.operation](
            local_path=args.local,
            remote_path=args.remote
        )
