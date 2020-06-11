'''
Created on 2020. jún. 11.

@author: Gabor Bergmann
'''
import unittest


class IQSJupyterExtensionsTest(unittest.TestCase):

    def testImport(self):
        import iqs_jupyter

    def testStatusOfDemoInstance(self):
        import iqs_jupyter
        
        iqs = iqs_jupyter.connect("https://openmbee.incquery.io", "openmbeeguest", "guest")
                
        status = iqs.server_management.get_server_status()
        
        self.assertIn('SERVER', status.component_statuses)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()