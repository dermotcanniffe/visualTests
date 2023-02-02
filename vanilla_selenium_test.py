import unittest
import os.path
from pathlib import Path
from selenium import webdriver
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from sbvt.visualtest import VisualTest
# API_KEY = 'BITBAR_API_KEY'
parentPath = Path(__file__).parent
resultsPath = os.path.join(parentPath, 'results')

chromedriver_autoinstaller.install()

class test_SeleniumTests(unittest.TestCase):
    "Self Tests"

    @classmethod
    def setUpClass(self):
        "Tests"
        settings = {
            'projectToken': 'Ma9MwAvV/Va0qvQf6eMg=',
            'saveTo': resultsPath,
            'debugImages': False,
            'debugLogs': False,
            'testRunName' : 'IronMan Test'
        }
        ###### For Chrome
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = ('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        # options.add_argument("--window-size=640,480")
        self.driver = webdriver.Chrome(options=options)

        ###### For Firefox
        # geckodriver_autoinstaller.install() 
        # self.driver = webdriver.Firefox(executable_path=r'c:\webdrivers\geckodriver.exe')

        self.driver.maximize_window()
        self.visualTest = VisualTest(self.driver, settings)


    def test_sanityTest(self):
        "Sanity Test to check page load"
        self.driver.get("https://demo.sanketh.io/")
        sleep(5), self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/div[1]/input").send_keys("dev@smartbear.com")
        sleep(5), self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/div[2]/input").send_keys("smartbear")
        self.driver.find_element_by_xpath("html/body/div[2]/div/div[1]/form/button").click()
        self.assertEqual(self.driver.title, "Awesome Shopping Store - Products")
        screenshot = self.visualTest.capture('Awesome Shopping Store - Products')
        print(f'Fullpage screenshot result: {screenshot}')

    def test_shopping(self):
        "Test to check product order"
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