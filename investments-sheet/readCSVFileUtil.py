#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#import io, os, sys
import pandas as pd
from constants import FILE_PATH

class ReadCSVFileUtil:

    def readFileCSV(fileName, usecols):
        if usecols == "ALL":
            return pd.read_csv(FILE_PATH+fileName, sep=";")
        return pd.read_csv(FILE_PATH+fileName, sep=";", header=0, usecols=usecols)
