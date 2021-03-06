link-validator
==============

Will recursively search and validate the HTTP response code of each link on a specified web page - and those of its children up - to the maximum specified recursion depth.

## Screenshot

![screenshot](https://github.com/at1as/at1as.github.io/blob/master/github_repo_assets/link-validate1.jpg)

## Usage

### Manual
Latest commits, but not thoroughly tested
* Download: `git clone https://github.com/at1as/link-validator.git`
* Run: `python link_validator_runner.py --url www.example.com --depth 2`
* See: `python link_validator_runner.py --help` for details

### Python Package
Older but more stable commits
* Download: `pip install link_validator`
* Run: `link_validator --url www.example.com --depth 2`
* See: `link_validator --help` for details
More package information [here](https://pypi.python.org/pypi/link_validator/0.2.3)

## Notes
* Tested and developed on Mac OS 10.10 with Python 2.7.6
* Recursion defautls to 2. Script will slow down a lot as this is increased


