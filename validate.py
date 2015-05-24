#!/usr/bin/python

import urllib2
import urlparse
import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored

# Notes:
# Will scan a page multiple times if different anchors are provided. 
# Requests isn't actually validating the anchors, so this is costly.


def get_broken_links(address, depth=1, max_depth=2):

  base_address_no_scheme = urlparse.urlparse(address).netloc
  base_address = urlparse.urlparse(address).scheme + '://' + base_address_no_scheme

  # Make the request, and save the DOM to extract links from
  r = requests.get(address, verify=False, allow_redirects=True)
  html_object = BeautifulSoup(r.text)

  # Find all links on the page
  for link in html_object.find_all('a'):

    # Extract href link from <a> tag
    try:
      inner_link = link.get('href')
      print "Link: %s" % inner_link
      print "Base Address: %s" % base_address
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
        print 'Result: multimedia address. Skipping.'
      else:
        try:
          link_follow = requests.get(inner_link, verify=False, allow_redirects=True)

          # Any HTTP code greater than or equal to 400 is flagged as erroneous
          if link_follow.status_code >= 400:
            broken_link_list.append([address, inner_link, link_follow.status_code])
            visited_links[inner_link] = link_follow.status_code
            print 'Result: ', inner_link, colored(': broken link', 'red'), link_follow.status_code
          else:
            print 'Result: ', inner_link, colored(': valid link', 'green')
            visited_links[inner_link] = link_follow.status_code

            # Recursively search pages until max_depth is reached
            if depth < max_depth:
              domain = urlparse.urlparse(inner_link).netloc
              print 'Recursion Depth: ' + str(depth) + ' < ' + str(max_depth)
              print 'inner link', inner_link
              print 'Domain: ' + str(domain)

              # Don't recuse external links or this will quickly diverge (i.e., social media links, etc)
              if base_address_no_scheme in domain:
                get_broken_links(inner_link, depth+1, max_depth)
                print 'Root: ' + str(base_address_no_scheme) + ' in ' + str(domain)
              else:
                print 'External Link ', colored('skipping', yellow)
            else:
              print 'Depth: Transcended %d / %d levels.' % (depth, max_depth),  colored('Stopping recusion', 'yellow')
        except: 
          print inner_link, ': not searchable ' + colored('uncontrolled failure', 'red')
    else:
      print 'Link does not contain an "href" tag ', colored('skipping', 'yellow')
    print '\n---\n'
  return broken_link_list


if __name__ == "__main__":
  
  broken_link_list = []
  visited_links = {}
  default_url = ""
  url = "http://www.w3.org/TR/html401/struct/links.html" # Add full URL beginning with "http://"
  
  print '\n'

  get_broken_links(url)


  # Compile Results
  print '----\nResults:'
  
  print '\n>> Visited Links'
  for link, status in sorted(visited_links.items(), key=lambda x: x[1]):
    if status == 200:
      print "%s => %s" %(link, colored(status, 'green'))
    elif status < 400:
      print "%s => %s" %(link, colored(status, 'yellow'))
    else:
      print "%s => %s" %(link, colored(status, 'red'))
  
  print '\n\n>> Broken Links'
  for broken_link in broken_link_list:
    print 'Origin : %s Link : %s => %s' %(broken_link[0], broken_link[1], colored(broken_link[2], 'red'))
  if len(broken_link_list) == 0:
    print 'None.'
  print '\n'
