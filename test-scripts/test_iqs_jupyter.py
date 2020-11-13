'''
Created on 2020. jún. 11.

@author: Gabor Bergmann
'''
import unittest


class IQSClientTest(unittest.TestCase):

    def testImport(self):
        import iqs_client


    '''
        Simple test courtesy of Ábel Hegedüs
    '''
    def testStatusOfDemoInstance(self):
        import iqs_client
        
        iqs_configuration = iqs_client.Configuration()
        iqs_configuration.host = "https://openmbee.incquery.io/api"
        iqs_configuration.username = "openmbeeguest"
        iqs_configuration.password = "guest"
        
        iqs = iqs_client.ApiClient(iqs_configuration)
        server_management_api = iqs_client.ServerManagementApi(iqs)
        
        status = server_management_api.get_server_status()
        
        self.assertIn('SERVER', status.component_statuses)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()