import inspect


myself = lambda: inspect.stack()[1][3]

class DriverForAllure:
    driver = None