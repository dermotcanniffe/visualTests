import unittest
import os
from pathlib import Path
from selenium import webdriver
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from sbvt.visualtest import VisualTest
# API_KEY = 'BITBAR_API_KEY'

API_KEY = os.environ.get('BITBAR_APIKEY') or ""
PROJECT_KEY = os.environ.get('VT_PROJECT_KEY') or "" 
parentPath = Path(__file__).parent
resultsPath = os.path.join(parentPath, 'results')

print("APIKEY: ", API_KEY, end='\n')
print("PROJECTKEY: ", PROJECT_KEY, end='\n')

chromedriver_autoinstaller.install()

class test_SeleniumTests(unittest.TestCase):
    "Self Tests"

    @classmethod
    def setUpClass(self):
        "Tests"

        ###### For BitBar
        # user-customizable parameters start here
        capabilities = {
            'platform': 'Linux',
            'osVersion': '18.04',
            'browserName': 'chrome',
            'version': '109',
            'resolution': '2560x1920',
        	'bitbar:options': 
            {
        		'apiKey': API_KEY,
        		'resolution': '2560x1920',
        		'osVersion': '18.04'
            },
        	'bitbar_project': 'Cloud Test',
        	'bitbar_testrun': 'Cloud Test Run',
        }

        # user-customizable parameters end here

        self.screenshot_dir = os.getcwd() + '/screenshots'

        self.driver = webdriver.Remote(command_executor='https://eu-desktop-hub.bitbar.com/wd/hub',
                                       desired_capabilities=capabilities)



        ###### For VT
        settings = {
            'projectToken': PROJECT_KEY,
            'saveTo': resultsPath,
            'debugImages': False,
            'debugLogs': False,
            'testRunName' : 'IronMan Test'
        }
        self.driver.maximize_window()
        self.visualTest = VisualTest(self.driver, settings)


    def test_sanityTest(self):
        "Sanity Test to check page load"
        self.driver.get("http://sb-se-international.northeurope.cloudapp.azure.com:9191/login.php")
        sleep(5), self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/div[1]/input").send_keys("sanketh.shanbhag@smartbear.com")
        sleep(5), self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/div[2]/input").send_keys("India@123")
        self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/button").click()
        self.assertEqual(self.driver.title, "Awesome Shopping Store - Products")
        screenshot = self.visualTest.capture('Awesome Shopping Store - Products')
        print(f'Fullpage screenshot result: {screenshot}')
        sleep(5), self.driver.find_element_by_xpath("html/body/div[2]/div/div[6]/div/div/div/div[2]/a").click()
        getProduct = self.driver.find_element_by_xpath("html/body/div/table/tbody/tr/td[1]").text
        self.assertEqual(getProduct, "iPhone")
        sleep(5), self.driver.find_element_by_xpath("/html/body/div/input").click()
        sleep(5), self.driver.find_element_by_xpath("/html/body/form[1]/div[1]/div[2]/a[2]").click()
        getMessage = self.driver.find_element_by_xpath("/html/body/div/p[1]").text
        self.assertEqual(getMessage, "Your order has submitted successfully.")
        screenshot = self.visualTest.capture('Your order has submitted successfully.')
        print(f'Fullpage screenshot result: {screenshot}')

    @classmethod
    def tearDownClass(self):
        "No more tests"
        sleep(5)
        self.driver.quit()

    #---START OF SCRIPT
if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(test_SeleniumTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
