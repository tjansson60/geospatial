#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve 2018-11-interactive-map.py
at your command prompt. Then navigate to the URL
    http://localhost:5006
in your browser.
'''

import pandas as pd
from pyproj import Proj, transform
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models.widgets import RangeSlider, MultiSelect, CheckboxButtonGroup, Button

# Convert from WGS84 (4326) to web mercator (3857)
proj_wsg84        = Proj('epsg:4326')
proj_wmerc        = Proj('epsg:3857')
callback_throttle = 1000  # ms

# Get position data
df = pd.read_parquet('data/small.parquet')
df = df.sample(5000)

# Make the UTM conversion of the positions
utmx, utmy = transform(proj_wsg84, proj_wmerc, df.lat.values, df.lon.values)
df['utmx'] = utmx
df['utmy'] = utmy

# Initial values
altitude_min = df.altitude_meters.min()
altitude_max = df.altitude_meters.max()

# Initial data
source = ColumnDataSource(data=dict(
    x        = df.utmx,
    y        = df.utmy,
    altitude = df.altitude_meters.values,
))

################
# Setup the plot
################
x_range = (df.utmx.median() - 2.5 * df.utmx.std(), df.utmx.median() + 2.5 * df.utmx.std())
y_range = (df.utmy.median() - 2.5 * df.utmy.std(), df.utmy.median() + 2.5 * df.utmy.std())

fig = figure(tools="hover,pan,wheel_zoom,save,reset",
        active_scroll='wheel_zoom',
        x_range=x_range,
        y_range=y_range,
        plot_width=1000,
        plot_height=700)
fig.axis.visible = False
fig.add_tile(get_provider(Vendors.STAMEN_TERRAIN))
fig.title.text = f'Positions shown: {df.shape[0]}'

# Plot the postions
fig.scatter('x', 'y', source=source)

# Setup the hover
hover = fig.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [("Altitude [m]", "@altitude")]

#################################
# Setup widgets
##################################
# widget_update_data = Button(label="Update data from database", button_type='success')
common_params = {'callback_policy': 'mouseup', 'callback_throttle': callback_throttle}

range_slider_altitude = RangeSlider(
    start=altitude_min,
    end=altitude_max,
    value=(altitude_min, altitude_max),
    step=50,
    title="Altitude", **common_params)
widget_list = [range_slider_altitude]


def update_selection_wrap_aon(attr, old, new):
    update_selection()


def update_selection(dummy=None):
    fig.title.text = "Updating positions positions based on altitude"

    # Update the data based on the selections
    altitude_min, altitude_max = range_slider_altitude.value

    # So this could easily be expanded with more checks
    df_temp = df.loc[(df['altitude_meters'].between(altitude_min, altitude_max, inclusive=True))]

    source.data    = dict(
        x          = df_temp.utmx,
        y          = df_temp.utmy,
        model_year = df_temp.altitude_meters.values,
    )

    # update title
    fig.title.text = "Positions shown: {}".format(len(df_temp.index))


for widget in widget_list:
    widget.on_change('value', update_selection_wrap_aon)

##############
# Setup layouy
##############
inputs_box  = widgetbox([
    # widget_update_data,
    range_slider_altitude,
])
curdoc().add_root(row(inputs_box, fig, width=800))
curdoc().title = "Positions visualization"
