# Goodlinks Exporter

A simple command-line utility which converts JSON exports from the [GoodLinks app](https://goodlinks.app/) to the input formats used by other bookmarking/read-it-later services (currently supports [Instapaper](https://www.instapaper.com/) and [Raindrop.io](https://raindrop.io/)).

## Introduction

In version 1.2.1 the GoodLinks app added the ability for users to export all links in their library. However, the resulting JSON file which GoodLinks generates is not compatible with the import tools of most major bookmarking/read-it-later services to which users might be interested in migrating. This utility takes care of that problem for Instapaper and Raindrop.io (other services may be supported in the future). However, the import tools and feature sets of each of the supported services have particualar limitations versus GoodLinks' own feature set; users are therefore **highly encouraged** to read the documentation below corresponding to their desired destination format prior to running this utility.

## General Usage

There are no third-party dependencies for this utility; however, the Python interpreter must be version 3.10 or higher.

After cloning into the repository, the command-line program can be executed as follows:

    usage: goodlinks-exporter.py -d/--destination {instapaper,raindrop} filename

Upon successful execution, the program will print a summary of the number of links which have been converted as well as the name of the output file which has been written to the working directory.

## Instapaper

### Instapaper Limitations

Instapaper's organizational tools are extremely limited. First of all it does not support tagging, which is the primary means of organization in GoodLinks. Instead it uses folders, with each saved link being able to live in only one folder at a time. In addition, archived links cannot be assigned to any folder at all. Instapaper *does* support a "Liked" category which roughly corresponds to the "Starred" featured in GoodLinks; however, Instapaper's import tool uses the same field for "Liked" as it does for "Folder" and "Archive", and only one value can be assigned to that field per link. This makes it extremely impractical to make use of the "Liked" category when importing items.

Given these considerable constraints, this tool has elected to make the following decisions when formatting for Instapaper:

* Read items in GoodLinks will be sent to the Archive folder in Instapaper (**tags will be ignored**).
* Unread items in GoodLinks with at least one tag will be sent to a folder in Instapaper equivalent to the **first** tag in GoodLinks (**all other tags will be ignored**).
* All other unread items in GoodLinks (i.e. those without tags) will be sent to the Home (i.e. "Unread") folder in Instapaper.
* **Stars on items in GoodLinks will be ignored** (users are free to manually mark these links as "Liked" in Instapaper after import).

### Instapaper Instructions

Once the user has generated an "instapaper-export.csv" file using this utility, they should navigate to the Settings page of their Instapaper account and scroll down until they reach the Import section. They should then click the "Import from Instapaper CSV" button to initiate the import into their account. Because this process is non-reversible, **users are highly encouraged to test the file generation and import process using a dummy account before doing so on their permanent account**.

## Raindrop.io

### Raindrop.io Limitations

Raindrop.io has a much richer feature set than Instapaper, and supports both tags and collections (i.e. folders). However, it does not currently support a native archived/marked-as-read status. Finally, while it supports a "Favorites" field corresponding to the "starred" status in GoodLinks, this field is not writable using the import tool. Therefore this tool has made the following choices when formatting for Raindrop.io:

* Read items in GoodLinks will be sent to a Raindrop.io collection called "Archive"
* Unread items in GoodLinks will be sent to a Raindrop.io collection called "Inbox"
* All tags will be transferred over
* **Stars on items in GoodLinks will be ignored** (users are free to manually mark these links as "Favorites" in Raindrop.io after import)

### Raindrop.io Instructions

Once the user has generated a "raindrop-export.csv" file using this utility, they should navigate to the Settings page of their Raindrop.io account and then choose the Import tab on the sidebar. After uploading the file, they will be given the option to either import everything, import only new items, or start from scratch by removing all existing links in their account and retaining only the imported items. Because each of these processes is non-reversible, **users are highly encouraged to test the file generation and import process using a dummy account before doing so on their permanent account**.
