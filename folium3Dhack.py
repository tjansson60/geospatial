#!/usr/bin/env python

import os
import folium
from folium.features import Template


class Map3d(folium.Map):

    def __init__(self, location=None, width='100%', height='100%', left='0%',
                 top='0%', position='relative', tiles='OpenStreetMap', API_key=None,
                 max_zoom=18, min_zoom=1, zoom_start=10, attr=None, min_lat=-90,
                 max_lat=90, min_lon=-180, max_lon=180, detect_retina=False, crs='EPSG3857'):
        super(Map3d, self).__init__(
            location=location, width=width, height=height,
            left=left, top=top, position=position, tiles=tiles,
            API_key=API_key, max_zoom=max_zoom, min_zoom=min_zoom,
            zoom_start=zoom_start, attr=attr, min_lat=min_lat,
            max_lat=max_lat, min_lon=min_lon, max_lon=max_lon,
            detect_retina=detect_retina, crs=crs
        )
        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <script src="https://www.webglearth.com/v2/api.js"></script>
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div class="folium-map" id="{{this.get_name()}}" ></div>
        {% endmacro %}

        {% macro script(this, kwargs) %}

            var southWest = L.latLng({{ this.min_lat }}, {{ this.min_lon }});
            var northEast = L.latLng({{ this.max_lat }}, {{ this.max_lon }});
            var bounds = L.latLngBounds(southWest, northEast);

            var {{this.get_name()}} = WE.map('{{this.get_name()}}', {
                                           center:[{{this.location[0]}},{{this.location[1]}}],
                                           zoom: {{this.zoom_start}},
                                           maxBounds: bounds,
                                           layers: [],
                                           crs: L.CRS.{{this.crs}}
                                         });
        {% endmacro %}
        """)


class TileLayer3d(folium.TileLayer):

    def __init__(self, tiles='OpenStreetMap', min_zoom=1, max_zoom=18, attr=None,
                 API_key=None, detect_retina=False, name=None, overlay=False, control=True):
        super(TileLayer3d, self).__init__(
            tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom,
            attr=attr, API_key=API_key, detect_retina=detect_retina,
            name=name, overlay=overlay, control=control
        )
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = WE.tileLayer(
                '{{this.tiles}}',
                {
                    maxZoom: {{this.max_zoom}},
                    minZoom: {{this.min_zoom}},
                    attribution: '{{this.attr}}',
                    detectRetina: {{this.detect_retina.__str__().lower()}}
                    }
                ).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)
