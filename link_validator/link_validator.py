#!/usr/bin/python

import urllib2
import urlparse
import argparse
import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning


# For storing results
# (better to keep lists outside of recursive function to avoid overwriting)
broken_link_list = []
visited_links = {}

# Print colored status code corresponding to severity of code
def print_colored_status(link, status):
  if status == 200:
    print "%s => %s" %(link, colored(status, 'green'))
  elif status < 400:
    print "%s => %s" %(link, colored(status, 'yellow'))
  else:
    print "%s => %s" %(link, colored(status, 'red'))


# Recurse links in page
def get_broken_links(address, max_depth=2, depth=1):
  
  base_address_no_scheme = urlparse.urlparse(address).netloc
  base_address = urlparse.urlparse(address).scheme + '://' + base_address_no_scheme
  user_agent = "Link Validator https://github.com/at1as/link-validator"

  # Make the request, and save the DOM to extract links from
  r = requests.get(address, verify=False, headers={'User-Agent':user_agent}, allow_redirects=True)
  html_object = BeautifulSoup(r.text)

  # Find all links on the page
  for link in html_object.find_all('a'):

    # Extract href link from <a> tag
    try:
      inner_link = link.get('href')
      print "Origin: %s" %address 
      print "Link: %s" % inner_link
      #print "Base Address: %s" % base_address
    except:
      pass
      
    if not inner_link is None:
      
      # Link Type. If the inner_link in the href tag isn't a full address, join it to the current address
      if inner_link and not inner_link.startswith('www') and not inner_link.startswith('http'):
        inner_link = urlparse.urljoin(address, inner_link)

      # Strip link anchor (i.e., www.example.com#heading1 => www.example.com)
      inner_link = inner_link.split('#')[0]

      # If link has been visited already, skip
      if visited_links.has_key(inner_link):
        print "Result: %s was already searched." %(inner_link), colored('Skipping.', 'yellow')

      # Skip testing multimedia links
      elif inner_link and ("mailto:" or "tel:") in inner_link:
        print 'Result: multimedia address. %s' %colored('Skipping.', 'yellow')
      else:
        try:
          link_follow = requests.get(inner_link, verify=False, headers={'User-Agent':user_agent}, allow_redirects=True)

          # Any HTTP code greater than or equal to 400 is flagged as erroneous
          if link_follow.status_code >= 400:
            broken_link_list.append([address, inner_link, link_follow.status_code])
            print "BLL: %s" %broken_link_list
            visited_links[inner_link] = link_follow.status_code
            print 'Result: ', inner_link, colored(': broken link', 'red'), link_follow.status_code
          else:
            print 'Result: ', inner_link, colored(': valid link', 'green')
            visited_links[inner_link] = link_follow.status_code

            # Recursively search pages until max_depth is reached
            if depth < max_depth:
              domain = urlparse.urlparse(inner_link).netloc
              print 'Depth: Transcended %d / %d levels' %(depth, max_depth)
              #print 'inner link', inner_link
              #print 'Domain: ' + str(domain)

              # Don't recuse external links or this will quickly diverge (i.e., social media links, etc)
              if base_address_no_scheme in domain:
                print '\n---\n'
                get_broken_links(inner_link, max_depth, depth+1)
              else:
                print 'External Link %s' %colored('stopping recursion', 'yellow')
            else:
              print 'Depth: Transcended %d / %d levels. %s' %(depth, max_depth, colored('Stopping recusion', 'yellow'))
        except Exception as e: 
          print '%s: not searchable %s Exception: %s' %(inner_link, colored('uncontrolled failure.', 'red'), e)
    else:
      print 'Link does not contain an "href" tag %s' %colored('skipping', 'yellow')
    print '\n---\n'
  return


def main():
  
  global broken_link_list
  global visited_links

  # Force disable SSL certificate verification
  requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
  requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
  
  # Parse Command Line Arguments
  parser = argparse.ArgumentParser(description='Recursive Link validator')
  parser.add_argument("--url", required=True, help='the url of the website to test against (ex. "http://www.w3.org/TR/html401/struct/links.html)')
  parser.add_argument("--depth", required=False, default=2, type=int, help='depth of recursion to search child links. Value > 2 will slow script down a lot (ex. 2)')
  args = parser.parse_args()
  user_args = vars(args)

  # If link starts with http or https skip, else append with http
  if not user_args['url'].lower().startswith("http"):
    user_args['url'] = "http://%s" %user_args['url']
  
  print '\n'

  get_broken_links(user_args['url'], user_args['depth'])

  # Display Results
  print '----\nResults:'

  print '\n>> Starting Link:\n%s' %user_args['url']

  print '\n>> Visited Links:'
  for link, status in sorted(visited_links.items(), key=lambda x: x[1]):
    print_colored_status(link, status)
  
  print '\n>> Broken Links:'
  for broken_link in broken_link_list:
    print 'Origin : %s Link : %s => %s' %(broken_link[0], broken_link[1], colored(broken_link[2], 'red'))
  if len(broken_link_list) == 0:
    print 'None!'
  
  print '\n'


if __name__ == "__main__":
  main()

