import sys
import csv

import pandas as pd

class CSV() :
    def __init__(self) :
        return

    @staticmethod
    def write_csv(csv_file, csv_map) :
        with open(csv_file,'w') as f:
            w = csv.writer(f)
            w.writerow(csv_map.keys())
            w.writerows(zip(*csv_map.values()))

    @staticmethod
    def append_csv(file_path, csv_map) :
        try : 
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(file_path) :
                with open(file_path,'w') as f:
                    w = csv.writer(f)
                    w.writerow(csv_map.keys())
            with open(file_path,'a', newline='') as f:
                w = csv.writer(f)
                for row in zip(*csv_map.values()) :
                    w.writerow(row)
        except Exception as e:
            print(f"[EXCEPT] during append_csv : {file_name}.\nexception : {e}")
            sys.stdout.flush()

    @staticmethod
    def read_csv(csv_file) :
        def row(*args):
            return map(list,zip(*args))

        res = list(csv.reader(open(csv_file,'r')))
        data = dict(zip(res[0],row(*res[1:])))    
        return data

class XLSX() :
    def __init__(self) :
        return
        
    @staticmethod
    def read_excel(excel_file, sheet_name) :
        return pd.read_excel(excel_file, sheet_name=sheet_name)


def test_package() :
    print("This is test package")