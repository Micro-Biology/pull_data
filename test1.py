import glob
import pathlib
import os
import Pandas as pd

class Well:
  """"Well information and metadata"""
  def __init__(self, loc, name, type, marker, ct, slope):
    self.loc = loc
    self.id = name
    self.type = type
    self.marker = marker
    self.ct = ct
    self.slop = slope
    
def xl_to_tsv(xl_path):
  path,xl = os.path.split(xl_path)
  csv,filetype = xl.split(".")
  csv = csv + ".csv"
  csv_path = os.path.join(path,csv)
  read_file = pd.read_excel (xl_path, sheet_name='Results') # probably best to put them somewhere else but this is fine for now
  read_file.to_csv (csv_path, index = None, header=True)
      
    
def import_runs(directory):
  dir_abspath = os.path.abspath(directory)
  xl_paths = glob.glob(str(dir_abspath)+"*/*.xls")
  for xl_path in xl_paths:
    xl_to_csv(file_path)
  csv_paths = glob.glob(str(dir_abspath)+"*/*.csv")
  for csv_path in cs_paths:
    with open(path) as csv:
      csv_reader = reader(csv)
      for row in csv_reader:
        print(row)
      
def get_args():
  parser = argeparse.ArgumentParser
  parser.add_argument("--input", help="Input folder name to look for qPCR data", required=True)
  return parser.parse_args()

def main():
  option = get_args()
  import_runs(options.input)

if __name__ == "__main__":
  main()
