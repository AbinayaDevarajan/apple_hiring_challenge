

import sys
import os
sys.path.append('../utils')
sys.path.append('../conf')
sys.path.append('../common')
sys.path.append('../src')
import installation_automation
from installation_automation import execute_automation



scenario1 = ("test_1", {
             "attribute": "..\data\test_partial.txt",
             "test_type": "load"}
)


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    print(argnames, argvalues)
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


def perform_test_automation(attribute):
    os.system('python ../src/installation_automation.py --input_file ../data/input_test.txt > out_result.dat')
    with open("out_result.dat","r") as in_file:
        arr = in_file.readlines()
        if (arr[2].lstrip().rstrip() == 'Installing  A' \
            and (arr[3].lstrip().rstrip() =='Installing  TELNET')):
            return True



class TestScenarioInstallAutomation:
    scenarios=[scenario1]

    def test_result(self, attribute, test_type):
        assert perform_test_automation(attribute)
        

    
