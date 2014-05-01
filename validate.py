#!/usr/bin/python

import urllib2
import urlparse
import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored

## Initialize
broken_link_list = []
visited_links = {}
default_url = ""

# Add full URL beginning with "http://"
url = "http://www.w3.org/TR/html401/struct/links.html"

#Current Limitations:
#Will scan a page multiple times if different anchors are provided. 
#Requests isn't actually validating the anchors, so this is costly.


def get_broken_links(address, depth=1, max_depth=2):
	global broken_link_list
	global visited_links
	base_address_no_scheme = urlparse.urlparse(address).netloc
	base_address = urlparse.urlparse(address).scheme + '://' + base_address_no_scheme

	# Make the request, and create an object (to extract tags from)
	r = requests.get(address, verify=False, allow_redirects=True)
	html_object = BeautifulSoup(r.text)

	for link in html_object.find_all('a'):
		print "Origin: ", address

		# Extract href link from <a> tag
		try:
			inner_link = link.get('href')
			print 'inner_link', inner_link
			print 'base_address', base_address
		except: pass
		
		if not inner_link is None:
			# Link Type. If the inner_link in the href tag isn't a full address, join it to the current address
			if inner_link and not inner_link.startswith('www') and not inner_link.startswith('http'):
				inner_link = urlparse.urljoin(address, inner_link)
			
			# If link has been visited already, skip
			if visited_links.has_key(inner_link):
				print inner_link, ': was already searched. Skipping.'

			# Unable to test multimedia links (for now)
			elif inner_link and ("mailto:" or "tel:") in inner_link:
				print 'multimedia address. Skipping.'
			else:
				try:
					link_follow = requests.get(inner_link, verify=False, allow_redirects=True)

					# For simplification, any HTTP code greater than 400 is flagged as erroneous
					if link_follow.status_code >= 400:
						broken_link_list.append([address, inner_link, link_follow.status_code])
						visited_links[inner_link] = link_follow.status_code
						print inner_link, colored(': broken link', 'red')
					else:
						print inner_link, colored(': valid link', 'green')
						visited_links[inner_link] = link_follow.status_code

						# Recursively search pages until max_depth is reached
						if depth < max_depth:
							domain = urlparse.urlparse(inner_link).netloc
							print str(depth) + ' < ' + str(max_depth)
							print 'inner link', inner_link
							print 'domain ' + str(domain)

							# Don't recuse external links or this will quickly diverge (i.e., social media links, etc)
							if base_address_no_scheme in domain:
								get_broken_links(inner_link, depth+1, max_depth)
								print 'root ' + str(base_address_no_scheme) + ' in ' + str(domain)
							else:
								print 'External link, skipping.'
						else:
							print 'transcended %d / %d levels.' % (depth, max_depth),  colored('Stopping recusion', 'yellow')
				except: 
					print inner_link, ': not searchable ' + colored('uncontrolled failure', 'red')
		else:
			print 'Link does not contain an "href" tag ', colored('skipping', 'yellow')
		print '---'
	return broken_link_list

##Broken Links
get_broken_links(url)


print '---- \n Visited Links \n', visited_links
print '---- \n Broken Links\n', broken_link_list
