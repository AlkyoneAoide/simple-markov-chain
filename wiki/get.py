# https://en.wikipedia.org/wiki/Python_(programming_language)
# https://www.mediawiki.org/wiki/API:Main_page

# 1. Get a plain text representation of either the entire page or the page "extract" straight from the API with the extracts prop

# Note that this approach only works on MediaWiki sites with the TextExtracts extension. This notably includes Wikipedia, but not some smaller Mediawiki sites like, say, http://www.wikia.com/

# You want to hit a URL like

# https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Bla_Bla_Bla&prop=extracts&exintro&explaintext

# Breaking that down, we've got the following parameters in there (documented at https://www.mediawiki.org/wiki/Extension:TextExtracts#query+extracts):

# action=query, format=json, and title=Bla_Bla_Bla are all standard MediaWiki API parameters
# prop=extracts makes us use the TextExtracts extension
# exintro limits the response to content before the first section heading
# explaintext makes the extract in the response be plain text instead of HTML
# Then parse the JSON response and extract the extract:

import sys
import requests
import mwparserfromhell

def program_help():
    print("Only takes one argument, the name of the wiki article as it is seen after 'wiki/' in the url")
    exit()

arg = sys.argv[1]

if (len(sys.argv) != 2 or arg == 'help' or arg == 'h'):
    program_help()

try:
    file = open("output", "x")
except FileExistsError:
    print("File output exists, delete it!")
    exit()

def extract_paragraph(arg):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': arg,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }).json()
    page = next(iter(response['query']['pages'].values()))
    # print(page['extract'])
    file.write(page['extract'])

# 3. Parse wikitext yourself
# You can use the query API to get the page's wikitext, parse it using mwparserfromhell (install it first using pip install mwparserfromhell), then reduce it down to human-readable text using strip_code. strip_code doesn't work perfectly at the time of writing (as shown clearly in the example below) but will hopefully improve.
def extract_page(arg):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': arg,
            'prop': 'revisions',
            'rvprop': 'content'
        }).json()
    page = next(iter(response['query']['pages'].values()))
    wikicode = page['revisions'][0]['*']
    parsed_wikicode = mwparserfromhell.parse(wikicode)
    # print(parsed_wikicode.strip_code())
    file.write(parsed_wikicode.strip_code())

extract_page(arg)
