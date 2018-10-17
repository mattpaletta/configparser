import json
import yaml
import argparse
import os


class Parser(object):
    def __init__(self, argparse_file: str,
                 config_file_key: str = None,
                 environ_key_mapping: Dict[str, str] = {}):
        assert os.path.exists(argparse_file), "Argparse file not found."
        self._argparse_file = argparse_file
        self._argparse_file_type = argparse_file.split(".")[-1]
        self._config_file_key = config_file_key
        self._environ_key_mapping: Dict[str, str] = environ_key_mapping

    def __get_os_environ(self):
        found_keys = {}
        for environ, config in self._environ_key_mapping.items():
            if environ in os.environ.keys():
                found_keys.update({config: os.environ[environ]})

        return found_keys

    def __get_args(self):
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

        # Arguments from command line and default values
        args = vars(parser.parse_args())
        # Only default values
        defaults = vars(parser.parse_args([]))

        parsed, unparsed = parser.parse_known_args()

        return parsed

    def _replace_args(self, old: dict, new: dict, p1: List[str], p2: List[str]):
        new_dict = {}
        for key, value in old:
            if type(val) is dict:
                if key in new.keys():
                    new_dict[key] = self._replace_args(old = value,
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

    def _layer_configs(self, runtime_configs):
        environ = self.__get_os_environ()
        config_files = self._config_file_key
        if type(config_files) is list:
            pass
        elif type(config_files) is str:
            pass


