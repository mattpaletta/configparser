import json
import logging
from typing import Dict

import yaml
import argparse
import os


class Parser(object):
    def __init__(self, argparse_file: str,
                 config_file_key: str = "",
                 environ_key_mapping: Dict[str, str] = {}):
        assert os.path.exists(argparse_file), "Argparse file not found."
        self._argparse_file = argparse_file
        self._config_file_key = config_file_key
        self._environ_key_mapping: Dict[str, str] = environ_key_mapping

    def get(self):
        return self._layer_configs()

    def __get_os_environ(self):
        found_keys = {}
        for environ, config in self._environ_key_mapping.items():
            if environ in os.environ.keys():
                found_keys.update({config: os.environ[environ]})

        return found_keys

    def __get_args(self):
        configs = self._load_config_file(self._argparse_file)

        arg_lists = []
        parser = argparse.ArgumentParser()

        # Dynamically populate runtime arguemnts.
        for g_name, group in configs.items():
            arg = parser.add_argument_group(g_name)
            arg_lists.append(arg)

            for conf, value in group.items():
                if "type" in value.keys():
                    if value["type"] == "int":
                        value["type"] = int
                    elif value["type"] == "str":
                        value["str"] = str
                arg.add_argument("--" + str(conf), **value)

        # Arguments from command line and default values
        args = vars(parser.parse_args())
        # Only default values
        defaults = vars(parser.parse_args([]))

        parsed, unparsed = parser.parse_known_args()

        return defaults, parsed.__dict__

    def _replace_args(self, old: dict, new: dict):
        def helper(old, new, p1, p2):
            new_dict = {}
            for key, value in old.items():
                if type(value) is dict:
                    if key in new.keys():
                        new_dict[key] = helper(old = value,
                                               new = new[key],
                                               p1 = p1.append(key),
                                               p2 = p2.append(key))
                    else:
                        new_dict[key] = value
                else:
                    if key in new.keys():
                        new_dict[key] = new[key]
                    else:
                        new_dict[key] = value
            return new_dict
        return helper(old, new, [], [])

    def _intercept_configs(self, old, new):
        def helper(old, new, p1, p2):
            new_dict = {}
            for key, value in old.items():
                if type(value) is dict:
                    if key in new.keys():
                        new_dict[key] = helper(old = value,
                                               new = new[key],
                                               p1 = p1.append(key),
                                               p2 = p2.append(key))
                    else:
                        new_dict[key] = value
                else:
                    if key in new.keys():
                        if new[key] != old[key]:
                            new_dict[key] = new[key]
                    else:
                        new_dict[key] = value
            return new_dict
        return helper(old, new, [], [])

    def _layer_configs(self):
        environ = self.__get_os_environ()

        logging.info("Getting defaults and runtime parameters")
        final_configs, runtime_configs = self.__get_args()

        runtime_configs = self._intercept_configs(final_configs, runtime_configs)

        if self._config_file_key is None:
            config_files_to_read = []
        elif os.path.exists(self._config_file_key):
            config_files_to_read = self._config_file_key
        elif self._config_file_key in runtime_configs.keys():
            config_files_to_read = runtime_configs[self._config_file_key]
        elif self._config_file_key in final_configs.keys():
            config_files_to_read = final_configs[self._config_file_key]
        else:
            config_files_to_read = []

        logging.info("Replacing with config files")
        # Replace with config files
        if type(config_files_to_read) is list:
            for f in config_files_to_read:
                final_configs = self._replace_args(old = final_configs,
                                                   new = self._load_config_file(f))
        elif type(config_files_to_read) is str:
            final_configs = self._replace_args(old = final_configs,
                                               new = self._load_config_file(config_files_to_read))

        if len(environ.keys()) > 0:
            logging.info("Replacing with environment variables.")
            final_configs = self._replace_args(old = final_configs,
                                               new = environ)
        if len(runtime_configs.keys()) > 0:
            logging.info("Replacing with runtime arguments.")
            final_configs = self._replace_args(old = final_configs,
                                               new = runtime_configs)

        return final_configs

    def _load_config_file(self, file_name):
        file_type = file_name.split(".")[-1]
        with open(file_name, "r") as file:
            if file_type == "json":
                configs = json.load(file)
            elif file_type in ["yaml", "yml"]:
                configs = yaml.load(file)
            else:
                raise NotImplementedError("File type not implemented")
        return configs
