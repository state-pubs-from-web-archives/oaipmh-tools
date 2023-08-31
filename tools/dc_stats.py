

"""dc_stats script for generating stats and visualizations"""

import argparse
from xml.etree import ElementTree
import sys
from collections import Counter
import texttable
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plt.switch_backend('WebAgg')

OAI_NAMESPACE = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
DC_NAMESPACE = "{http://purl.org/dc/elements/1.1/}"


class RepoInvestigatorException(Exception):
    """This is our base exception for this script"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


def graph(file_name):

    meta_element = ["title", "creator", "contributor",
                    "publisher", "date", "language",
                    "description", "subject", "coverage",
                    "source", "relation", "rights", "type",
                    "format", "identifier"]

    final = {}
    val = {}
    c = 0
    d = 0
    for m_e in meta_element:
        total_count = 0
        count = 0
        element_counter = Counter()
        values_dict = Counter()
        try:
            for _event, elem in ElementTree.iterparse(file_name):
                if elem.tag == "record":
                    element_count = 0
                    total_count += 1
                    try:
                        for element in elem[1][0]:
                            if element.tag == DC_NAMESPACE + m_e:
                                element_count += 1
                                values_dict[element.text] += 1
                        if element_count > 0:
                            element_counter[element_count] += 1
                            count += 1
                    except:
                        pass
        except:
            pass
        element_counter[0] = total_count - count
        val[m_e] = values_dict
        if len(element_counter) != 0:
            final[m_e] = element_counter
    for elem in final:
        k = list(final[elem].keys())
        v = list(final[elem].values())
        k = max(k)
        v = max(v)
    fig, axs = plt.subplots(3, 5, figsize=(19, 10))
    fig.tight_layout(pad=5.0)
    fig.suptitle('Stas Graphs(log-scale) for ' + file_name.split("/")[-1])
    for elem in final:
        if d == 5:
            d = 0
            c += 1
        k = list(final[elem].keys())
        v = list(final[elem].values())
        k_l = [i for i in k if i != 0]
        v_l = [math.log10(i) for i in v if i != 0]
        for j in range(len(k_l)):
            axs[c][d].text(x=k_l[j], y=v_l[j], s=str(k[j])+" : "+str(v[j]),
                           ha='left',  rotation=90, fontsize=6)
            axs[c][d].vlines(k_l[j], ymax=v_l[j], ymin=0, linewidth=1)
            axs[c][d].set_title(elem.capitalize())
        axs[c][d].set_ylim(bottom=0, top=int(max(v_l)+1))
        axs[c][d].set_xlim(left=-1)
        axs[c][d].set_xlabel("Number of "+elem, fontsize=8)
        axs[c][d].set_ylabel("Count [Log-Scale]", fontsize=8)
        axs[c][d].xaxis.set_major_locator(MaxNLocator(integer=True))
        axs[c][d].yaxis.set_major_locator(MaxNLocator(integer=True))
        axs[c][d].tick_params(axis='both', labelsize=8)
        ax2 = axs[c][d].twinx()
        ax2.set_yscale('log')
        ax2.text(x=0, y=final[elem][0], s=str(0)+" : "+str(final[elem][0]),
                 ha='left',  rotation=90, fontsize=6)
        ax2.vlines(0, ymax=final[elem][0], ymin=0, linewidth=1, color='r')
        ax2.set_yticks([10**i for i in axs[c][d].get_yticks()])
        ax2.set_ylabel("Count [Normal-Scale]", fontsize=8)
        gini = gini_coeff(list(val[elem].values()))
        entropy = calc_entropy(val[elem])
        x_ticks = axs[c][d].get_xticks()
        y_ticks = ax2.get_yticks()
        le = 0
        ri = 0
        indi = -1
        for i in range((len(x_ticks) + 1) // 2):
            if x_ticks[i] == x_ticks[indi]:
                if (final[elem][x_ticks[i]] > y_ticks[-1] or
                        final[elem][x_ticks[i]] > y_ticks[-2]):
                    ri = 1
            if (final[elem][x_ticks[i]] > y_ticks[-1] or
                    final[elem][x_ticks[i]] > y_ticks[-2]):
                le = 1
            if (final[elem][x_ticks[indi]] > y_ticks[-1] or
                    final[elem][x_ticks[indi]] > y_ticks[-2]):
                ri = 1
            if le == 1 or ri == 1:
                break
            indi -= 1
        print(elem, ":", le, ri)
        if le == 0 and ri == 1:
            axs[c][d].legend(bbox_to_anchor=(0.4, 1), title="\nGini : "
                             + str(round(gini, 2)) + "\nEntropy : "
                             + str(round(entropy, 2)), prop={"size": 0.01})
        elif le == 1 and ri == 0:
            axs[c][d].legend(bbox_to_anchor=(1, 1), title="\nGini : "
                             + str(round(gini, 2)) + "\nEntropy : "
                             + str(round(entropy, 2)), prop={"size": 0.01})
        else:
            axs[c][d].legend(bbox_to_anchor=(0.4, 1), title="\nGini : "
                             + str(round(gini, 2)) + "\nEntropy : "
                             + str(round(entropy, 2)), prop={"size": 0.01})
        r = -1
        for i in range(15 - len(final)):
            axs.flat[r].set_visible(False)
            r -= 1
        plt.grid(axis='y')
        print(elem.capitalize()+" is processed")
        d += 1
    plt.show()


def gini_coeff(x):
    g = 0.5 * ((np.abs(np.subtract.outer(x, x)).mean())/np.mean(x))
    return g


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
    try:
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
    except:
        mode_freq = round((freq_count / total_count)*100, 2)
    return mode_freq


def stats_main(r_element, file_name):
    total_count = 0
    neg_count = 0
    count = 0
    values_dict = Counter()
    element_counter = Counter()
    try:
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
                    neg_count += 1
                    continue
        total_count = total_count - neg_count
        if len(values_dict) == 0 and len(element_counter) == 0:
            return [total_count + neg_count, neg_count,
                    r_element, 0, "0%", 0, 0, 0, "0%", 0, 'None']

        p_with_element_instances = round((count / total_count) * 100, 2)
        unique_values = len(values_dict)
        mean_instances_r = mean(element_counter)
        mode_instances_r = mode(element_counter)
        mode_freq = mode_frequency(r_element, mode_instances_r,
                                   total_count, file_name)
        Entropy = calc_entropy(values_dict)
        gini = gini_coeff(list(values_dict.values()))
    except:
        total_count = total_count - neg_count
        if len(values_dict) == 0 and len(element_counter) == 0:
            return [total_count + neg_count, neg_count,
                    r_element, 0, "0%", 0, 0, 0, "0%", 0, 'None']

        p_with_element_instances = round((count / total_count) * 100, 2)
        unique_values = len(values_dict)
        mean_instances_r = mean(element_counter)
        mode_instances_r = mode(element_counter)
        mode_freq = mode_frequency(r_element, mode_instances_r,
                                   total_count, file_name)
        Entropy = calc_entropy(values_dict)
        gini = gini_coeff(list(values_dict.values()))
        print(count, total_count)
        print("hi")

    return [total_count + neg_count, neg_count,
            r_element, count, str(p_with_element_instances)+"%",
            unique_values, mean_instances_r,
            *mode_instances_r, str(mode_freq)+"%", Entropy, gini]


def main():
    """Main file handling and option handling"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stats", action="store_true",
                        dest="stats", default=False,
                        help="Stats for each metadata elements")
    parser.add_argument("-v", "--visualization", action="store_true",
                        dest="visu", default=False,
                        help="visualizations for each metadata elements")
    parser.add_argument("filename", type=str,
                        help="OAI-PMH Repository File")

    args = parser.parse_args()

    if args.stats is False and args.visu is False:
        parser.print_help()
        sys.exit(1)

    if args.visu is True:

        file_name = args.filename
        graph(file_name)

    if args.stats is True:
        t_count = 0
        n_count = 0
        file_name = args.filename
        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.HEADER)
        table.set_cols_align(["l", "r", "r", "r", "r", "r", "r", "r", "l"])
        table.set_cols_width([14, 14, 14, 14, 14, 14, 14, 14, 14])

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
                   "Frequency of Mode Instances Per Records",
                   "Entropy", "Gini_Coefficient"]
        rows = []
        rows.append(headers)
        for element in meta_element:
            values = stats_main(element, file_name)
            t_count = values[0]
            n_count = values[1]
            rows.append(values[2:])

        table.add_rows(rows)
        print(table.draw())
        if n_count != 0:
            print('\tTotal_records : {0}\n \tDeleted_records : {1}\
                  \n \tAvailable_records : {2}\
                  '.format(t_count, n_count, t_count-n_count))
        else:
            print('\tTotal_records and\
                  Available_records : {0}'.format(t_count))


if __name__ == "__main__":
    main()
