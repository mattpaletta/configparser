# configparser
Simplified runtime configs for Python

[![Build Status](https://travis-ci.com/mattpaletta/configparser.svg?branch=master)](https://travis-ci.com/mattpaletta/configparser)


Examples can be seen in `examples/`

To use configparser:
`pip install git+git://github.com/mattpaletta/configparser.git`


You can call it in your program using:
```
p = Parser(argparse_file = "argparse.yml").get()
```

The paramters are:
- argparse_file: your argparse definitions, layed out in JSON or yaml files.
- config_file_key: a string to the optional config file key in the argparse file to use to allow the user to run custom runtime config files.
- environ_key_mapping: a dictionary containing the config file key to the environment key (bash environment)

The arguments will be applied on top of each other in the following order:

1. defaults
2. config files (in the order defined)
3. environment variables
4. runtime

This order cannot be modified at this time.
