# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:32:23 2020

@author: Arjun Acharya
"""

import glassdoor_scraper as gs
import pandas

path = 'C:/ChromeDriver/chromedriver'
df = gs.get_jobs('data scientist', 1000, False, path, 15)

df.to_csv("glassdoor_job.csv", index = False)

