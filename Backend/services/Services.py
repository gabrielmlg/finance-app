import pyspark
from pyspark import SparkContext
import json

sc = SparkContext()

print("====================")
print('Spark version: {}'.format(sc.version))
print('Python version: {}'.format(sc.pythonVer))
print("====================")

def extract():
    json_stock = sc.textFile('/Users/gabriel/Documents/dev/finance-projects/notebooks/data_raw/ibov-MGLU3.json')
    json_stock.first()




