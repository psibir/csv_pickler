
import os
import argparse
import csv
import pickle
import gzip

class CSVtoPickleConverter:
    def __init__(self, delimiter=","):
        self.delimiter = delimiter

    def csv_to_pickle(self, input_path, output_path):
        with open(input_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter)
            data = [row for row in reader]

        with gzip.open(output_path, "wb") as pickle_file:
            pickle.dump(data, pickle_file)

    def pickle_to_csv(self, input_path, output_path):
        with gzip.open(input_path, "rb") as pickle_file:
            data = pickle.load(pickle_file)

        with open(output_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delimiter)
            for row in data:
                writer.writerow(row)


class BulkConverter:
    def __init__(self, input_path, output_path, converter):
        self.input_path = input_path
        self.output_path = output_path
        self.converter = converter

    def convert(self):
        if os.path.isdir(self.input_path):
            for file_name in os.listdir(self.input_path):
                input_file_path = os.path.join(self.input_path, file_name)
                output_file_path = os.path.join(self.output_path, f"{os.path.splitext(file_name)[0]}.pickle.gz")
                self.converter.csv_to_pickle(input_file_path, output_file_path)
        else:
            self.converter.csv_to_pickle(self.input_path, self.output_path)

    def convert_reverse(self):
        if os.path.isdir(self.input_path):
            for file_name in os.listdir(self.input_path):
                input_file_path = os.path.join(self.input_path, file_name)
                output_file_path = os.path.join(self.output_path, f"{os.path.splitext(file_name)[0]}.csv")
                self.converter.pickle_to_csv(input_file_path, output_file_path)
        else:
            self.converter.pickle_to_csv(self.input_path, self.output_path)


def main():
    parser = argparse.ArgumentParser(description="Convert CSV files to Pickle files and vice versa.")
    parser.add_argument("--delimiter", default=",", help="Delimiter character used in the CSV file.")
    parser.add_argument("--compress", action="store_true", help="Compress the output pickle file with gzip.")
    parser.add_argument("--reverse", action="store_true", help="Convert from pickle to CSV instead of CSV to pickle.")
    parser.add_argument("input_path", help="Path to the input CSV or pickle file or directory.")
    parser.add_argument("output_path", help="Path to the output pickle or CSV file or directory.")
    args = parser.parse_args()

    if args.compress:
        pickle_extension = ".pickle.gz"
    else:
        pickle_extension = ".pickle"

    if args.reverse:
        converter = CSVtoPickleConverter(args.delimiter)
        bulk_converter = BulkConverter(args.input_path, args.output_path, converter)
        bulk_converter.convert_reverse()
    else:
        converter = CSVtoPickleConverter(args.delimiter)
        bulk_converter = BulkConverter(args.input_path, args.output_path, converter)
        bulk_converter.convert()


if __name__ == "__main__":
    main()
