import glob
import pathlib
import os
import pandas as pd
from csv import reader

analysts = ["GK","WS","MC","TC","JG","AB","JC","JR","]
qpcrs = ["ainsely","brian","charlie","dennis","erica","fry","graham","harriet","igor","jupiter"]
robots = ["TRO","KEN","HOY","CAV","PEN","WIG","FRO"]

class Well:
  """"Well information and metadata"""
  def __init__(self, run_name, time, row):
    self.fin_time = time
    run_name_list = run_name.split()
    for part in run_name_list:
      if part[0:2] == "21":
        self.daydate = part
      if part[0:2] in analysts:
        try:
          self.analysts = self.analysts.append(part)
        except AttributeError:
          self.analysts = [part]
    self.loc = row[1]
    self.id = row[3]
    self.marker = row[4]
    self.type = row[5]
    self.reporter = row[6]
    if row[8] == "Undetermined":
      self.ct = "No Cq"
    else:
      self.ct = row[8]
    if row[11] == "":
      self.gc = 0
    else:
      self.gc = float(row[11])
    self.yint = row[14]
    self.r2 = row[15]
    self.eff = row[16]
    self.threshold = row[18]


def xl_to_csv(xl_path):
  path,xl = os.path.split(xl_path)
  csv,filetype = xl.split(".")
  csv = csv + ".csv"
  csv_path = os.path.join(path,csv)
  read_file = pd.read_excel (xl_path, sheet_name='Results') # probably best to put them somewhere else but this is fine for now
  read_file.to_csv (csv_path, index = None, header=True)
      
    
def import_runs(directory):
  well_data = []
  dir_abspath = os.path.abspath(directory)
  xl_paths = glob.glob(str(dir_abspath)+"/*/*.xls")
  for xl_path in xl_paths:
    xl_to_csv(xl_path)
  csv_paths = glob.glob(str(dir_abspath)+"/*/*.csv")
  for csv_path in csv_paths:
    with open(csv_path) as csv:
      csv_reader = reader(csv)
      i = 0
      for row in csv_reader:
        i=i+1
        if i == 33:
          run_name = row[1]
        if i == 29:
          time = row[1]
        if i > 47:
          well_data.append(Well(run_name, time, row))
  return well_data

      
def get_args():
  parser = argeparse.ArgumentParser
  parser.add_argument("--input", help="Input folder name to look for qPCR data", required=True)
  return parser.parse_args()

def main():
  #option = get_args()
  well_data = import_runs("subset")
  for well in well_data:
    print(well.gc)

if __name__ == "__main__":
  main()