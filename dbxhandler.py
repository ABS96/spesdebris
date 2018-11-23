import dropbox

class DropboxHandler:

  def __init__(self, apikey):
    self.dbx=dropbox.Dropbox(apikey,timeout=30)

  # Dropbox download
  # syntax: getfile source [destination]
  def get_file(self, c):
    cs = c.split(" ", 1)
    source_file = cs[0]
    print("Getting {} from Dropbox...".format(source_file))
    dest_file = cs[1] if len(cs) > 1 else "C:\\Downloads\\" + source_file

    try:
      self.dbx.files_download_to_file(dest_file, "/" + source_file)
    except dropbox.exceptions.ApiError:
      print("Error: file cannot be found!")
      return
    print("File has finished downloading to {}".format(dest_file))

    print("Removing from cloud...")
    try:
      self.dbx.files_delete_v2("/" + source_file)
    except dropbox.exceptions.ApiError:
      print("Error: file cannot be deleted!")
      return
    print("Done")

  def upload_file(self):
    pass
    # TODO