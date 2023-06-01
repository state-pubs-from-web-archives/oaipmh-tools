"""dc_breaker script for processing OAI-PMH 2.0 Repository XML Files"""

import argparse
from xml.etree import ElementTree
import sys
from collections import Counter
import texttable
import math


OAI_NAMESPACE = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"


class RepoInvestigatorException(Exception):
    """This is our base exception for this script"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


def calc_entropy(x):

    if len(x) == 1:
        return 0.0

    my_sum = 0
    counts = x
    total = 0
    for s in x:
        total += int(x[s])

    if total == 0:
        return 0.0

    probs = []
    for k in x:
        new = x[k] / total
        probs.append(new)

    for p in probs:
        if p > 0:
            my_sum += p * math.log(p) / math.log(len(counts))

    return -round(my_sum, 3)


def mean(data_dict):
    sum_values = 0
    freq_values = 0
    for key, value in data_dict.items():
        val = int(key) * value
        sum_values += val
        freq_values += value
    mean = sum_values // freq_values
    return mean


def mode(data_dict):
    val = max(list(data_dict.values()))
    mode_val = [key for key, value in data_dict.items() if value == val]
    return mode_val


def mode_frequency(r_element, mode, total_count, file_name):
    freq_count = 0
    for _event, elem in ElementTree.iterparse(file_name):
        if elem.tag == "record":
            element_count = 0
            try:
                for element in elem[1][0]:
                    if element.tag == DC_NAMESPACE + r_element:
                        element_count += 1
                if element_count in mode:
                    freq_count += 1
            except:
                continue
    mode_freq = round((freq_count / total_count)*100, 2)
    return mode_freq


def stats_main(r_element, file_name):
    total_count = 0
    count = 0
    values_dict = Counter()
    element_counter = Counter()

    for _event, elem in ElementTree.iterparse(file_name):
        if elem.tag == "record":
            total_count += 1
            element_count = 0
            try:
                for element in elem[1][0]:
                    if element.tag == DC_NAMESPACE + r_element:
                        element_count += 1
                        values_dict[element.text] += 1
                if element_count > 0:
                    count += 1
                    element_counter[element_count] += 1
            except:
                continue
    if len(values_dict) == 0 and len(element_counter) == 0:
        return [r_element, 0, "0%", 0, 0, 0, "0%", 0]

    p_with_element_instances = round((count / total_count) * 100, 2)
    unique_values = len(values_dict)
    mean_instances_r = mean(element_counter)
    mode_instances_r = mode(element_counter)
    mode_freq = mode_frequency(r_element, mode_instances_r,
                               total_count, file_name)
    Entropy = calc_entropy(values_dict)

    return [r_element, count, str(p_with_element_instances)+"%",
            unique_values, mean_instances_r,
            *mode_instances_r, str(mode_freq)+"%", Entropy]


def main():
    """Main file handling and option handling"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stats", action="store_true",
                        dest="stats", default=False,
                        help="Stats for each metadata elements")
    parser.add_argument("filename", type=str,
                        help="OAI-PMH Repository File")

    args = parser.parse_args()

    if args.stats is False:
        parser.print_help()
        sys.exit(1)

    if args.stats is True:
        file_name = args.filename
        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.HEADER)
        table.set_cols_align(["l", "r", "r", "r", "r", "r", "r", "l"])

        meta_element = ["title", "creator", "contributor",
                        "publisher", "date", "language",
                        "description", "subject", "coverage",
                        "source", "relation", "rights", "type",
                        "format", "identifier"]
        headers = ["Element Name", "Records with Element Instances",
                   "Percentage of Records with Element Instances",
                   "Unique data Values in Element",
                   "Mean Element Instances Per Record",
                   "Mode Element Instances Per Record",
                   "Frequency of Mode Instances Per Records", "Entropy"]
        rows = []
        rows.append(headers)
        for element in meta_element:
            values = stats_main(element, file_name)
            rows.append(values)

        table.add_rows(rows)
        print(table.draw())


if __name__ == "__main__":
    main()
