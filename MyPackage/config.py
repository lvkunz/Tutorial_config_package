import numpy as np
import os

class Config:
    def __init__(self, file_name):

        config_dict = self.read_config_file(file_name)

        self.__dict__ = {**self.__dict__, **config_dict}

        #TODO: here you can add rules for your parameters if needed (type checking, etc.)

        #if the seed is set to -1, generate a random seed
        if self.seed == -1:
            self.seed = np.random.randint(0, 1000000)

        #add an extra parameter to the class that is the working directory of the package
        self.working_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def read_config_file(self, file_name):
        config_dict = {}
        file_name = file_name + '.txt'

        with open(file_name, 'r') as f:
            for line in f:
                # Remove comments and strip leading/trailing whitespaces
                line = line.split('#')[0].strip()

                # Skip blank lines
                if not line:
                    continue

                key, value = line.split(': ')

                # Check if the value is a number (integer or float)
                if value.replace('.', '', 1).isdigit() or value.lstrip('-').replace('.', '', 1).isdigit():
                    if '.' in value:
                        config_dict[key] = float(value)
                    else:
                        config_dict[key] = int(value)
                # Check if the value is a boolean
                elif value.lower() == 'true' or value.lower() == 'false':
                    config_dict[key] = bool(value.lower() == 'true')
                # Otherwise, treat the value as a string
                else:
                    config_dict[key] = value

        return config_dict