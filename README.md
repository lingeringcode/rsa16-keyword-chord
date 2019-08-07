# RSA16 Twitter Data Analysis

## Processing data

1. #RSA16 [data source](data/source/rsa16-tweets-full-0531.csv): TAGSExplorer hashtag-based archiving from Lauren Kersey as CSV.
2. Converted the CSV to a JSON file with the [conversion script](data/source/csvtojson.py).
3. Generated overall word counts of entire archive with [wordcount.py](data/process/wordcount.py).
4. Based on the word counts, I created the [#RSA16 Bubble Clouds](rsa16bubble/index.html).
5. Based on top keywords and my own substantive experiences at RSA16, I generated numerous keyword tallies in the [data/process/output](data/process/output) folder with the goal to develop Sankey diagrams, such the following [sankey-topwords.html](sankey-topwords.html).
6. After generating the Sankey, I noticed some keyword overlapping patterns and decided to make some similar visualizations by [merging](data/process/merge-csv-files.py) desired keyword files to make chord diagrams to highlight the overlaps.

    ### keyword data issues

        - Tense: disability vs. disabilities, machine vs. machines, etc. All of these can be consolidated in the tallying process with regex, but I then need to consolidate them in the "related" column in the CSV.
        - Multiple words in one subject area: able / disabled, embodied / embodiment / body/ies.
        - In lieu of these insights/boundaries, I developed a cleaning script for the "related" column after merging desired keyword files. (See next step #7)
7. [more to come]