# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:54:52 2022

@author: JH218595
"""
import skrf as rf
import numpy as np
import pandas as pd
from io import StringIO
from skrf.io.citi import Citi
from skrf.io.mdif import Mdif

ex_1p_1 = Mdif('test_1p_gmdif.mdf').to_networkset()

#%%
ex_1p_1.to_mdif('test.mdf')
