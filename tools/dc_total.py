"""dc_total script for processing OAI-PMH 2.0 Repository XML Files into .csv file"""

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


def create_vector(file_name):
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
                    p = element
                    element = element.tag.split("}")
                    element = element[1].strip()
                    if element not in vector:
                        vector[element] = p.text 
                    else :
                        vector[element] = vector[element] + " *** " + p.text
            except :
                pass
            instances = ["record_id", "title", "creator", "contributor",
                        "publisher", "date", "language",
                        "description", "subject", "coverage",
                        "source", "relation", "rights", "type",
                        "format", "identifier"]
            for instance in instances :
                if vector[instance] == 0:
                    vector[instance] = 0
                else:
                    try:
                        vector[instance] = vector[instance].split('***')
                    except:
                        vector[instance] = 0
            '''print ([vector["record_id"],
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
                    vector["identifier"]])'''

            
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
    parser.add_argument("-t", "--binary_vector", action="store_true",
                        dest="bin_vect", default=False,
                        help="Binary Representation of metadata elements\
                        for each record whether they are present or not")
    parser.add_argument("filename", type=str,
                        help="OAI-PMH Repository File")

    args = parser.parse_args()
    if args.bin_vect is False :
        parser.print_help()
        sys.exit(1)

    if args.bin_vect:
        c = 0
        for record in create_vector(args.filename):
            df.loc[len(df.index)] = record
            c += 1
        print(c)
        df.to_csv(args.filename+'.csv')
if __name__ == "__main__":
    main()
