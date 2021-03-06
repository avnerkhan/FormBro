# When run, this file gets output.json, and places at all into one set where there is only one URL to read. Easy
# Works assuming clean.json and output.json are present and have data
import sys
import os
sys.path.append(os.getcwd() + "/..")
from util import read_and_load, write_to_file

data = read_and_load("output.json")
old_clean_data = read_and_load("clean.json")
new_clean_data = set([piece["file_urls"][0]
                      for piece in data] + [clean["url"] for clean in old_clean_data])
new_clean_data = [{"url": url} for url in new_clean_data]
print(len(new_clean_data))
write_to_file("clean.json", new_clean_data)
