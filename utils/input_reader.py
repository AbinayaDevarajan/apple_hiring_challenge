
import sys
sys.path.append('../utils')
sys.path.append('../conf')
sys.path.append('../common')
from exceptions import InstallationAutomationFileException

class InputReader():
    def __init__(self,input_path):
        self.input_path = input_path
    def read_input(self):
        try:
            with open(self.input_path, 'r') as input_file:
                    input_contents = input_file.readlines()
                    return [item .strip() for item in input_contents]
        except (IndexError,IOError):
            raise InstallationAutomationFileException("Cannot read the input file")
            
 

