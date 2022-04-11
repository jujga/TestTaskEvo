      my Portfolio
1. Preparing environment :
   - Using Pycharm install dependencies via terminal: `pip install -r requirements.txt`
   - Using recommendations in the `https://docs.qameta.io/allure/#_installing_a_commandline` install Allure                          
2. Running tests (using Pycharm's terminal or cmd):
     `venv\Scripts\pytest.exe --alluredir=<YOUR DIR> -m ui` - run only IU tests
     `venv\Scripts\pytest.exe --alluredir=<YOUR DIR> -m rest` -run only api tests
     `venv\Scripts\pytest.exe --alluredir=<YOUR DIR>` - run all tests
          where `<YOUR DIR>` is a local or network path to allure files storage
3. Getting report (using Pycharm's terminal or cmd):
     `allure serve <YOUR DIR>`
