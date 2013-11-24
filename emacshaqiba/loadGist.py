import urllib2
import json
import re

api_github_url = "https://api.github.com/gists/"

def load_gist(gist_url):
    response = urllib2.urlopen(api_github_url + extract_gist_id(gist_url))
    data = json.load(response)
    for item in data["files"].values():
        return item["content"]

def extract_gist_id(gist):
    """Extract gist Id from GitHub gist url.
    
    This function is copied from
    https://gist.github.com/spencerogden/4702275
    
    Arguments:
    - `gist`: GitHub gist url.

    """
    if re.match(r'^([0-9a-f]+)$', gist):
        return gist
    m = re.match(r'^http(s?)://gist.github.com/([^/]+/)?([0-9a-f]*)', gist)
    if m:
        return m.group(3)
    m = re.match(r'^http(s?)://raw.github.com/gist/([0-9a-f]*)', gist)
    if m:
        return m.group(2)

# Usage:
# print load_gist("https://gist.github.com/psachin/6386902")

