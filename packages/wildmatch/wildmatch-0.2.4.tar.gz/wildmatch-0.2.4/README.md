`wildmatch`
-----------

This CLI tool is intended to assist in filtering lists of paths by potentially arbitrary `.gitignore`-like configuration
files. It uses the [`python-pathspec`](https://github.com/cpburnz/python-path-specification) library with `argparse` to
allow easier use in pipelines and automation.
```shell
$ wildmatch --help
usage: wildmatch [-h] [-c CONF] [-i INPUT]

Filter lists of paths by arbitrary .gitignore-like configuration files.

options:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  optionally set the configuration file to filter by, defaults to .diffignore
  -i INPUT, --input INPUT
                        optionally specify an input file to filter by the configuration file
```

### Install

Installation requires Python v3.10 or later.
```
pip install wildmatch
```
