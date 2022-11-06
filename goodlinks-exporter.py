import argparse
from csv import DictWriter
import json
from math import trunc
from os import path
from re import sub
import sys


def main():
    # Configure command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--destination",
        choices=["instapaper", "raindrop"],
        help="destination format",
        required=True,
    )
    parser.add_argument("filename", help="JSON file exported by GoodLinks")
    args = parser.parse_args()
    # Verify input file is a JSON
    file, ext = path.splitext(args.filename)
    if ext.lower() != ".json":
        sys.exit("error: input file must have a .json extension")
    # Verify input file exists
    if path.exists(args.filename) is False:
        sys.exit("error: input file not found")

    # Call function to parse JSON and return a list of links
    links = parse_json(args.filename)

    # Send links to specified conversion function if one exists
    format = args.destination
    match format:
        case "instapaper":
            instapaper(links)
        case "raindrop":
            raindrop(links)


def parse_json(file):
    """
    Parse a GoodLinks JSON file into a list.

    :param file: JSON file exported by GoodLinks
    :raise json.JSONDecodeError: if JSON format is invalid
    :raise IOError: if file cannot be opened
    :return: a list containing each object in the JSON array
    :rtype: list
    """
    try:
        with open(file) as f:
            try:
                links = json.load(f)
            except json.JSONDecodeError:
                sys.exit("error: could not parse JSON file")
            return links
    except IOError:
        sys.exit(f"error: could not open {file}")


def instapaper(links):
    """
    Convert a list of links to an Instapaper CSV file.

    The provided list of links is formatted for Instapaper and written to
    a CSV file. Untagged links are marked for either the "Archive" or
    "Unread" folders in Instapaper (depending on read status), tagged
    links are stored in a folder corresponding to the first tag, and URLs
    and timestamps are cleaned for compatibility.

    :param links: a list of links to be writen to a CSV file
    :type links: list
    :raise IOError: if the file cannot be successfully opened for writing
    :rtype: None
    """
    filename = "instapaper-export.csv"
    try:
        with open(filename, "w") as file:
            linkcount = 0
            # Define CSV columns required by Instapaper's import tool
            fields = ["URL", "Title", "Selection", "Folder", "Timestamp"]
            writer = DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for link in links:
                # Determine what folder to save each link into
                if "readAt" in link:
                    # If the link is read then archive it
                    folder = "Archive"
                elif link["tags"] != []:
                    # If the link is tagged then put it in a folder named
                    # for the first tag.
                    folder = link["tags"][0]
                else:
                    # Put unread and untagged links into the "Unread" folder
                    folder = "Unread"
                # Clean up timestamp and URL
                created = striptime(link["addedAt"])
                url = cleanurl(link["url"])

                # Write final link output to CSV row
                writer.writerow({"URL": url, "Folder": folder, "Timestamp": created})
                linkcount += 1
            success(linkcount, filename)
    except IOError:
        sys.exit(f"error: could not write to {filename}")


def raindrop(links):
    """
    Convert a list of links to a Raindrop.io CSV file.

    The provided list of links is formatted for Instapaper and written to
    a CSV file. Links are marked for either "Archive" or "Inbox" folders in
    Raindrop.io, tags are converted from a list to a single string, and URLs
    and timestamps are cleaned for compatibility.

    :param links: a list of links to be written to a CSV file
    :type links: list
    :raise IOError: if the file cannot be successfully opened for writing
    :rtype: None
    """
    filename = "raindrop-export.csv"
    try:
        with open(filename, "w") as file:
            linkcount = 0
            # Define CSV columns required by Raindrop's import tool
            fields = ["url", "folder", "title", "description", "tags", "created"]
            writer = DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for link in links:
                # Determine what folder to save each link into
                if "readAt" in link:
                    # If the link is read put it in an Archive folder
                    folder = "Archive"
                else:
                    # Otherwise put it in an Inbox folder
                    folder = "Inbox"
                # Concatenate tags into a single string
                tags = ", ".join(link["tags"])
                # Clean the timestamp and URL
                created = striptime(link["addedAt"])
                url = cleanurl(link["url"])

                # Write final link output to CSV row
                writer.writerow(
                    {"url": url, "folder": folder, "tags": tags, "created": created}
                )
                linkcount += 1
            success(linkcount, filename)
    except IOError:
        sys.exit(f"error: could not write to {filename}")


def striptime(datetime):
    """Remove time suffix from Unix timestamps."""
    return trunc(datetime)


def cleanurl(link):
    """Clean positional suffixes from saved URLs."""
    return sub(r"\#.*", "", link)


def success(linkcount, filename):
    """Print a success summary message and exit with status 0."""
    print(f"Successfully converted {linkcount} links and saved output as '{filename}'.")
    sys.exit(0)


if __name__ == "__main__":
    main()
