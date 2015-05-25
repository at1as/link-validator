link-validator
==============

Will recursively search and validate the HTTP response code of each link on a specified web page - and those of its children up - to the maximum specified recursion depth.

## Screenshot

![screenshot](https://github.com/at1as/at1as.github.io/blob/master/github_repo_assets/link-validate1.jpg)

## Usage

* Download: `git clone https://github.com/at1as/link-validator.git`
* Run: `python validate.py --url www.example.com --depth 2`
* See: `python validate.py --help` for details
 
## Notes
* Tested and developed on Mac OS 10.10 with Python 2.7.6
* Recursion defautls to 2. Script will slow down a lot as this is increased

