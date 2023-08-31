
"""dc_vector script for generating binary and total vectors"""

import argparse
from xml.etree import ElementTree
import sys
from collections import Counter
import pandas as pd

OAI_NAMESPACE = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"


class RepoInvestigatorException(Exception):
    """This is our base exception for this script"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


def create_vector(file_name, option):
    record_id = ""
    for _event, elem in ElementTree.iterparse(file_name):
        if elem.tag == "record":
            vector = Counter()
            try:
                record_id = elem.find("header/identifier").text
                vector["record_id"] = record_id
            except AttributeError as err:
                raise RepoInvestigatorException(
                                                "Record does not have\
                                                a valid Identifier") from err
            try:
                for element in elem[1][0]:
                    element = element.tag.split("}")
                    element = element[1].strip()
                    if option == 'c':
                        vector[element] += 1
                    else:
                        if element not in vector:
                            vector[element] += 1
            except:
                yield ([vector["record_id"],
                        vector["title"],
                        vector["creator"],
                        vector["contributor"],
                        vector["publisher"],
                        vector["date"],
                        vector["language"],
                        vector["description"],
                        vector["subject"],
                        vector["coverage"],
                        vector["source"],
                        vector["relation"],
                        vector["rights"],
                        vector["type"],
                        vector["format"],
                        vector["identifier"]])
                continue
            yield ([vector["record_id"],
                    vector["title"],
                    vector["creator"],
                    vector["contributor"],
                    vector["publisher"],
                    vector["date"],
                    vector["language"],
                    vector["description"],
                    vector["subject"],
                    vector["coverage"],
                    vector["source"],
                    vector["relation"],
                    vector["rights"],
                    vector["type"],
                    vector["format"],
                    vector["identifier"]])


def main():
    """Main file handling and option handling"""

    df = pd.DataFrame(columns=["record_id", "title", "creator", "contributor",
                               "publisher", "date", "language",
                               "description", "subject", "coverage",
                               "source", "relation", "rights", "type",
                               "format", "identifier"])
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--binary_vector", action="store_true",
                        dest="bin_vect", default=False,
                        help="Binary Representation of metadata elements\
                        for each record whether they are present or not")
    parser.add_argument("-c", "--count_vector", action="store_true",
                        dest="count_vect", default=False,
                        help="Count representation of individual\
                        metadata element for each record whether\
                        they are present or not")
    parser.add_argument("filename", type=str,
                        help="OAI-PMH Repository File")

    args = parser.parse_args()
    if args.bin_vect is False and args.count_vect is False:
        parser.print_help()
        sys.exit(1)

    if args.bin_vect:
        for record in create_vector(args.filename, 'b'):
            df.loc[len(df.index)] = record
            print(record)
        df.to_csv(args.filename.split(".")[0]+".csv")

    if args.count_vect:
        c = 0
        for record in create_vector(args.filename, 'c'):
            df.loc[len(df.index)] = record
            print(record)
            c += 1
        print(c)
        df.to_csv(args.filename.split(".")[0]+".csv")


if __name__ == "__main__":
    main()
