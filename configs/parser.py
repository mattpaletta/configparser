import json
import yaml
import argparse
import os


class Parser(object):
    def __init__(self, argparse_file: str,
                 config_file_key: str = None,
                 environ_key_mapping: Dict[str, str] = None):
        assert os.path.exists(argparse_file), "Argparse file not found."
        self._argparse_file = argparse_file
        self._argparse_file_type = argparse_file.split(".")[-1]
        self._config_file_key = config_file_key
        self._environ_key_mapping = environ_key_mapping

    def get_args(self):
        with open(self._argparse_file, "r") as file:
            if self._argparse_file_type == "json":
                configs = json.load(file)
            elif self._argparse_file_type in ["yaml", "yml"]:
                configs = yaml.load(file)
            else:
                raise NotImplementedError("File type not implemented")

        arg_lists = []
        parser = argparse.ArgumentParser()

        # Dynamically populate runtime arguemnts.
        for g_name, group in configs.items():
            arg = parser.add_argument_group(g_name)
            arg_lists.append(arg)

            for conf in group.keys():
                arg.add_argument("--" + str(conf), **group[conf])

        parsed, unparsed = parser.parse_known_args()

        return parsed