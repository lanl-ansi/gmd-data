# Methods to download query results to files.
#
import csv
from json import dumps
'''
    Python 2 style enum for specifyting output format.
'''
class OutputType:
    CSV = "csv"
    JSON = "json"

'''
    Class writes query results to selected file formats.
'''
class MeasurementsWriter:

    def __init__(self, path, prefix, output_type):
        self.output_type = output_type
        if (self.output_type == OutputType.CSV):
            self.filepath = path+"/"+prefix+".csv"
            self.file = open(self.filepath, 'w')
            self.writer = csv.writer(self.file)
        elif (self.output_type == OutputType.JSON):
            self.filepath = path+"/"+prefix+".json"
            self.file = open(self.filepath, 'w')
            self.writer = self.file

    def writeMeasurements(self,rs):
        metadata = rs._metadata
        self.column_names = list(metadata.keys)
        self.firstrecord = True
        for row in  rs:
            if (self.output_type == OutputType.CSV):
                if self.firstrecord:
                    self.writer.writerow(self.column_names)
                    self.firstrecord = False
                self.writer.writerow(row)
            elif (self.output_type == OutputType.JSON):
                if self.firstrecord:
                    self.file.write('[')
                    self._write_JSON_row_object(row)
                    self.firstrecord = False
                else:
                    self.file.write(',')
                    self._write_JSON_row_object(row)
        rs.close()

    def _write_JSON_row_object(self,rsrow): # Writes a single row from an SQLAlchemy ResultProxy to the file.
        rowobj = {}
        for c in self.column_names:
            value = rsrow[c]
            if (c=="date_utc"):
                value = str(value)
            rowobj[c] = value
        self.file.write(dumps(rowobj))


    def close(self):
        if(self.output_type == OutputType.JSON):
            self.file.write(']')
        self.file.close()