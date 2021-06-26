import glob
import pathlib
import os
import pandas as pd
from csv import reader
import csv

analysts = ["GK","WS","MC","TC","JG","AB","JC","JR","DS","JK","SM","AW","SG","DH","VD","CV","GM","JD","JT","JH","LR","JW","NE",
            "CE","DJ","BS","CA","CO","JS","KM","SXB","AP","NF","SB","FH","JS","IR","JS","FG","JV","RH","BM","ROM"]
qpcrs = ["ainsely","brian","charlie","dennis","erica","fry","graham","harriet","igor","jupiter"]
robots = ["TRO","KEN","HOY","CAV","PEN","WIG","FRO"]
types = ["UNKNOWN","STANDARD","NTC"]
markers = ["N1","Phi6","CrAssphage"]

class Well:
  """"Well information and metadata"""
  def __init__(self, run_name, time, row):
    self.time = time
    run_name_list = run_name.split()
    self.instrument = "Unknown"
    self.robot = "Unknown"
    for part in run_name_list:
      if str(part[0:2]) == "21":
        self.daydate = str(part)
      if str(part).upper() in analysts:
        try:
          self.analysts = self.analysts.append(str(part).upper())
        except AttributeError:
          self.analysts = [str(part).upper()]
      if str(part).lower() in qpcrs:
        self.instrument = str(part[0:3]).upper()
      if str(part[0:3]).upper() in robots:
        self.robot = str(part[0:3]).upper()
    self.loc = str(row[1])
    self.id = str(row[3])
    self.marker = str(row[4])
    self.type = str(row[5])
    self.reporter = str(row[6])
    if row[8] == "Undetermined":
      self.ct = "No Cq"
    else:
      self.ct = str(float(row[8]))
    if row[11] == "":
      self.gc = "0"
    else:
      self.gc = str(float(row[11]))
    self.yint = str(float(row[14]))
    self.r2 = str(float(row[15]))
    self.eff = str(float(row[16]))
    try:
      self.thresh = str(float(row[19]))
    except ValueError:
      print(run_name +" "+str(row[19]))
      self.thresh = "False"

def get_args():
  parser = argeparse.ArgumentParser
  parser.add_argument("--input", help="Input folder name to look for qPCR data", required=True)
  return parser.parse_args()

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

def subset_data_marker(wells, marker):
  wells_subset = []
  for well in wells:
    if well.marker == marker:
      wells_subset.append(well)
  return wells_subset

def subset_data_type(wells, type):
  wells_subset = []
  for well in wells:
    if well.type == type:
      wells_subset.append(well)
  return wells_subset
      
def save_data(wells):
  for marker in markers:
    marker_subset = subset_data_marker(wells, marker)
    for type in types:
      print("Saving " + marker + " " + type + "s")
      type_subset = subset_data_type(marker_subset, type)
      file_name = marker + "_" + type +"s.csv"
      file = open(file_name,"w")
      writer = csv.writer(file)
      writer.writerow(["id","loc","type","marker","ct","gc","y-int","r2","threshold","time","instrument","robot","analysts"])
      for well in type_subset:
        line = [well.id,well.loc,well.type,well.marker,well.ct,well.gc,well.yint,well.r2,well.thresh,well.time,well.instrument,well.robot]
        for analyst in well.analysts:
          line.append(analyst)
        writer.writerow(line)
      file.close()


def main():
  #option = get_args()
  well_data = import_runs("subset")
  save_data(well_data)

if __name__ == "__main__":
  main()