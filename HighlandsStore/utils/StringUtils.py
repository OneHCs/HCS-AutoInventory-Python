from GlobalImports import *

class StringUtils:
    @staticmethod
    def convert_to_float(value):
        try:
            return round(float(value), 4)
        except ValueError:
            return value