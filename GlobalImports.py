import os
import sys
import json
import requests
import pyperclip
from io import StringIO
import argparse
from urllib.parse import urlencode
from collections import defaultdict
import csv
import pandas as pd
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
from HighlandsStore.LoginHandler import LoginHandler
from HighlandsStore.services.HighlandsAPIService import HighlandsAPIService
from HighlandsStore.utils.ExcelHandler import ExcelHandler
from HighlandsStore.EndpointHandling.EndpointConstants import EndpointConstants
from HighlandsStore.EndpointHandling.EndpointHandler import EndpointHandler
from HighlandsStore.SecretsEnvHandler import SecretsEnvHandler
from HighlandsStore.StoreIdHandler import StoreIdHandler
from HighlandsStore.dataclass.StoreDTO import StoreDTO
import random,string
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from HighlandsStore.dataclass.ItemDTO import ItemDTO
from HighlandsStore.TransferHandler import TransferHandler
from HighlandsStore.utils.ExcelHandler import ExcelHandler
from HighlandsStore.utils.StringUtils import StringUtils
from HighlandsStore.InventoryService import InventoryService
from HighlandsStore.InventoryHandler import InventoryHandler
from HighlandsStore.LstDetailHandler import LstDetailHandler
from HighlandsStore.utils.ExcelTFHandler import ExcelTFHandler