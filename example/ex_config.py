from configs import Parser

if __name__ == "__main__":
    p = Parser(argparse_file = "argparse2.yml",
               config_file_key = "config").get()
    print(p)
    print("You entered: {0} + {1} = {2}".format(p["a"],
                                                p["b"],
                                                p["a"] + p["b"]))
