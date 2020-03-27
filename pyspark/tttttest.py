# -*- coding: utf-8 -*-
'''
@Time    : 2019/6/12 15:53
@Author  : shangyf
@File    : tttttest.py
'''
import pandas as pd
import numpy as np

if __name__ == "__main__":
    import plotly_express as px

    gapminder = px.data.gapminder()
    gapminder2007 = gapminder.query('year == 2007')
    px.scatter(gapminder2007, x='gdpPercap', y='lifeExp')