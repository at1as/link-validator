link-validator
==============

Will recursively validate each link on a specified website, and those of its children.

## Screenshot

![screenshot](https://github.com/at1as/at1as.github.io/blob/master/github_repo_assets/link-validate1.jpg)

## Usage

* `git clone https://github.com/at1as/link-validator.git`
* Modify the url variable included in validate.py to a link of your choosing, and run the script. Recursion depth defaults to 2, but can be set in the get_broken_links function arguments. Things slow down a lot as this increases, so start low
* python validate.py

## Notes
* Tested on Mac OS 10.10 with Python 2.7

