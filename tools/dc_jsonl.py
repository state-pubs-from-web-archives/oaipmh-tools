"""dc_jsonl script for generating jsonl metadata for each existing record"""

import argparse
from xml.etree import ElementTree
import sys
from collections import Counter
import json
OAI_NAMESPACE = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"


class RepoInvestigatorException(Exception):
    """This is our base exception for this script"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


def create_vector(file_name):
    for _, elem in ElementTree.iterparse(file_name):
        if elem.tag == "record":
            vector = Counter()
            header = Counter()
            try:
                for element in elem[0]:
                    if element.tag not in header:
                        header[element.tag] = element.text
                    else:
                        try:
                            header[element.tag] = header[element.tag] + [element.text]
                        except:
                            header[element.tag] = [header[element.tag]] + [element.text]

                for element in elem[1][0]:
                    p = element
                    element = element.tag.split("}")
                    element = element[1].strip()
                    if element not in vector:
                        vector[element] = [p.text]
                    else:
                        vector[element] = vector[element] + [p.text]
            except IndexError:
                continue
            '''for instance in instances:
                if vector[instance] == 0:
                    vector[instance] = 0
                else:
                    continue'''

            yield vector, header


def main():
    """Main file handling and option handling"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json_vector", action="store_true",
                        dest="json_vect", default=False,
                        help="provides data in JSON formate")
    parser.add_argument("filename", type=str,
                        help="OAI-PMH Repository File")

    args = parser.parse_args()
    if args.json_vect is False:
        parser.print_help()
        sys.exit(1)

    if args.json_vect:
        for record, record2 in create_vector(args.filename):
            record_f = Counter()
            record_f['header'] = dict(record2)
            record_f['metadata'] = dict(record)
            print(json.dumps(record_f))


if __name__ == "__main__":
    main()
