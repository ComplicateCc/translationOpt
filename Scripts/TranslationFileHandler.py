# -*- coding: utf-8 -*-

import hashlib
import itertools
import json
import os
import csv
import re
import sqlite3
import uuid
import pandas as pd
import DataStructure
from DataCollection import clean_and_extract_text
from difflib import SequenceMatcher  #比较库
from tqdm import tqdm  #进度条library

from SQLDataBase import create_connection, create_table
from TranslationTemplateData import CleanStrData, TranslationTemplateData 

