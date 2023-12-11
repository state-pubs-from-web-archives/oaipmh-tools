# oaipmh-tools
Scripts and tools for transforming the output from OAI-PMH repositories.

# Overview of Tools
We have four distinct kinds of scripts (tools) in this repository: dc_jsonl.py, dc_stats.py, and dc_vector.py.
1. The dc_jsonl.py tool enables us to harvest metadata as JSON Lines rather than XML. Each line of the data that was captured reflects a record's accessible metadata in a particular repository.
2. The dc_stats.py script enables us to locate the fundamental statistics and fundamental visualizations on the obtained metadata. The fundamental statistics include the number of records with existing instances, their percentage, the unique data values in each instance's existing metadata, the mean element instances per record, the mode instances per record, the frequency of the mode instances per record, the entropy and the Gini coefficients. It provides a summary of the records currently in existence for each metadata instance for visualization.
3. The dc_vector.py script allows us to create binary and count vectors, two different types of vectors for metadata analysis. To indicate the existence of the metadata instances for each record, a binary vector of length 15 signifies either 1 or 0. Count vector is another vector of length 15, where each count represents the number of distinct metadata instances for each record that are known to exist.
4. dc_total.py script uses the harvested metadata which is in xml format and then it convert those xml file into .csv formate where each column represent the unique dubline core metadata instance(i.e., record_id, title, creator, contributor, publisher, date, language, description, subject, coverage, source, relation, rights, type, format, identifier) and row represents the each document metadata.
## dc_jsonl.py
dc_jsonl.py script help us to harvest the metadata using in the form of JSON Lines using the harvested XML with the help of [pyoai_harvester.py](https://github.com/vphill/pyoaiharvester). It has two different flags which are -j flag to generate json data and -h for help.

**Modules :**
  > [*argparse*](https://docs.python.org/3/library/argparse.html)
    [*sys*](https://docs.python.org/3/library/sys.html)
    [*ElementTree*](https://docs.python.org/3/library/xml.etree.elementtree.html)
    [*Counter*](https://docs.python.org/3/library/collections.html#collections.Counter)

**Usage :**
In linux :
* For Json data 
```bash
 python3 dc_jsonl.py -j [-file_name]
 ```
 * For help
 ```bash
 python3 dc_jsonl.py -h
 ```
 ## dc_stats.py
This Scrpit help us to find some interesting stats on our metadata elements. It gives output ASCII texttable which conatins 15 rows and 7 columns where rows are 15 metadata elements("title", "creator", "contributor", "publisher", "date", "language", "description", "subject", "coverage", "source", "relation", "rights", "type", "format", "identifier") and columns are ("Element Name", "Records with Element Instances", "Percentage of Records with Element Instances", "Unique data Values in Element", "Mean Element Instances Per Record", "Mode Element Instances Per Record", "Frequency of Mode Instances Per Records") using -s flag. It also provides basic visualization charts using -v flag.

**Modules :**
  > [*argparse*](https://docs.python.org/3/library/argparse.html)
    [*sys*](https://docs.python.org/3/library/sys.html)
    [*ElementTree*](https://docs.python.org/3/library/xml.etree.elementtree.html)
    [*Counter*](https://docs.python.org/3/library/collections.html#collections.Counter)
    [*texttable*](https://pypi.org/project/texttable/)
    [*math*](https://docs.python.org/3/library/math.html)
    [*numpy*](https://wiki.python.org/moin/NumPy)
    [*matplotlib*](https://pypi.org/project/matplotlib/)

**Usage :**
In linux :
* For stats
``` bash
python3 dc_stats.py -s [-file_name]
```
* For visualizations
``` bash
python3 dc_stats.py -v [-file_name]
```
* For help
``` bash
python3 dc_stats.py -h
```
## dc_vector.py
dc_stats.py provide 2 options for the user to findout more about metadata. Firstly, it provide vector with binary representation of metadata instances for every record in the xml document with the help of '-b'  flage. Next, it provide the count vector for each metadata instances in xml document with the help of '-c' flage.

**Modules :**
  > [*argparse*](https://docs.python.org/3/library/argparse.html)
    [*sys*](https://docs.python.org/3/library/sys.html)
    [*ElementTree*](https://docs.python.org/3/library/xml.etree.elementtree.html)
    [*Counter*](https://docs.python.org/3/library/collections.html#collections.Counter)
    [*pandas*](https://pypi.org/project/pandas/)

**Usage :**
In linux :
* For Binary Vector
```bash
 python3 dc_vector.py -b [-file_name]
 ```
 * For Count Vector
 ```bash
 python3 dc_vector.py -c [-file_name]
 ```
 * For help
 ```bash
 python3 dc_vector.py -h
 ```
## dc_total.py
dc_total.py provide 1 option for the user to download harvested metadata into .CSV file. We can downlaod these file using '-t' flag.

**Modules :**
  > [*argparse*](https://docs.python.org/3/library/argparse.html)
    [*sys*](https://docs.python.org/3/library/sys.html)
    [*ElementTree*](https://docs.python.org/3/library/xml.etree.elementtree.html)
    [*Counter*](https://docs.python.org/3/library/collections.html#collections.Counter)
    [*pandas*](https://pypi.org/project/pandas/)

**Usage :**
In linux :
* To download total vector
```bash
 python3 dc_total.py -t [-file_name]
 ```
* For help
 ```bash
 python3 dc_total.py -h
 ```

Here the input file should be the harvested metadata which is in xml format.
