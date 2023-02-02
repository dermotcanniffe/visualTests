import os.path
import time, unittest, sys, argparse
from pathlib import Path
from selenium import webdriver
from sbvt.visualtest import VisualTest
from packaging import version as semver
import chromedriver_autoinstaller

PROJECT_TOKEN = 'p6v069dX/W185DWYWfrA='
testName = 'python test run'
url = 'https://www.google.com'

# will be defined in args
browser = None
resolution = None
case = None

topPath = Path(__file__).parent.parent.parent.parent.parent  # the "test" folder
parentPath = Path(__file__).parent
driversPath = os.path.join(topPath, 'webdrivers')
resultsPath = os.path.join(parentPath, 'results')
chromedriver_autoinstaller.install()


class TestLocalQuickTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('---- Starting functional test: TestLocalQuickTest ----')

        cls.urls = None
        cls.driver = None

    def setUp(self):
        print(f'Selenium version installed is {webdriver.__version__}')
        selVersion = semver.parse(webdriver.__version__)
        print(f'Launching webdriver for {browser}')
        if selVersion >= semver.parse('4.0.0'):
            if browser == 'chrome':
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.binary_location = ('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
                self.driver = webdriver.Chrome(options=options)
                self.driver.maximize_window()
            elif browser == 'firefox':
                from selenium.webdriver.firefox.service import Service
                service = Service(os.path.join(driversPath,'geckodriver'), log_path=os.path.join(topPath,'python','logs','geckodriver.log'))
                self.driver = webdriver.Firefox(service=service)
            elif browser == 'safari':
                from selenium.webdriver.safari.service import Service
                service = Service()
                self.driver = webdriver.Safari(options=service)
            else:
                print(f'No webdriver available for {browser}')
                quit()
        elif selVersion >= semver.parse('3.0.0'):
            if browser == 'chrome':
                self.driver = webdriver.Chrome()
            elif browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif browser == 'safari':
                self.driver = webdriver.Safari()
            else:
                print(f'No webdriver available for {browser}')
                quit()
        # self.driver.maximize_window()
        self.driver.set_window_size(resolution[0], resolution[1])
        size = self.driver.get_window_size()
        print(f'Window size is now: {size}')

    def tearDown(self):
        print(f'closing webdriver for {browser}')
        self.driver.quit()

    def testViewportScreenshot(self):
        print(f'testViewportScreenshot method running')

        scrollMethod = 'JS_SCROLL'

        print(
            f'>>> TESTCASE: Name={testName.upper()} Browser={browser} ScreenResolution={resolution[0]}x{resolution[1]}<<<')

        settings = {
            'projectToken': 'p6v069dX/W185DWYWfrA=',
            'saveTo': resultsPath,
            'debugImages': False,
            'debugLogs': False
        }
        visualTest = VisualTest(self.driver, settings)
        visualTest.scrollMethod = scrollMethod

        # load the url
        print(f'Opening URL: {url}')
        self.driver.get(url)
        time.sleep(1)

        # take a viewport screenshot
        result = visualTest.capture(f'quicktest-{testName}-viewport-screenshot', {'viewport': True})
        print(f'capture result: {result}')

        # is height of image generated within 1px of expected height based on javascript fullpage?
        tolerance = 1
        heightWithinTolerance = result['imageSize']['height'] - tolerance <= result['expectedSize']['height'] <= \
                                result['imageSize']['height'] + tolerance
        self.assertTrue(heightWithinTolerance, f'Fullpage image height was NOT within {tolerance}px of expected height')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--browser', default='chrome', type=str)
    parser.add_argument('-r', '--resolution', default='1366x768', type=str)
    parser.add_argument('-t', '--testcase', default='all', type=str)
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args

    browserOptions = ["firefox", "chrome", "safari"]
    # browser = webdriver.Firefox()
    browser = args.browser.lower()
    print(f'browser to test: {browser}')
    if browser not in browserOptions:
        raise Exception(f'Must provide command line argument of browser. \nOptions: {browserOptions}')

    res = args.resolution.split('x')
    resolution = (int(res[0]), int(res[1]))
    print(f'resolution to test: {resolution[0]}x{resolution[1]} ')

    case = args.testcase
    print(f'testcase to run is: {case} ')
    try:
        unittest.main()
    except Exception as e:
        print(f'Error starting test {e}')
