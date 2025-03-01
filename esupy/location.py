# location.py (esupy)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to facilitate creation of location objects
"""

import bz2
import json
import pandas as pd
from pathlib import Path

from esupy.remote import make_url_request

path = Path(__file__).parent

# %% get GeoJSON
url = 'https://geography.ecoinvent.org/files'
# https://geography.ecoinvent.org/#id12

location_dict = {'states': 'states.geojson.bz2',
                 'countries': 'countries.geojson.bz2',
                 'us_electricity': ['usa-electricity.geojson.bz2',
                                    'electricity.geojson.bz2']}

def extract_coordinates(group) -> dict:
    """
    Creates a dictinary of locations, where the key is the location code
    and the values are 'geometry': geoJSON coordinates and 'properties': dict
    """
    file = location_dict.get(group)
    if file is None:
        raise KeyError(f'Must select group from available '
                       f'keys: {list(location_dict.keys())}')
    if isinstance(file, str):
        file = [file]
    features = []
    for f in file:
        response = make_url_request(f'{url}/{f}')
        content = bz2.decompress(response.content)
        data = json.loads(content)
        # extract GeoJSON objects from the FeatureCollection
        features.extend(data['features'])

    ## need to also grab the UUID?
    if group in ('states', 'us_electricity'):
        d = {f['properties']['shortname']: {'geometry': f['geometry'],
                                            'properties': f['properties']}
                     for f in features
                     if f['properties']['shortname'].startswith('US')}
    else:
        d = {f['properties']['shortname']: {'geometry': f['geometry'],
                                            'properties': f['properties']}
             for f in features}
    return d

def olca_location_meta():
    location_meta = ('https://raw.githubusercontent.com/GreenDelta/'
                     'data/master/refdata/locations.csv')
    df = pd.read_csv(location_meta)
    return df


def assign_state_abbrev(df):
    """
    Replaces state FIPS with state abbreviations, e.g., "US-AL" in the
    "Location" column. Also assigns "00000" to "US".
    Requires flowsa
    """
    try:
        import flowsa
    except ImportError:
        raise ImportError("assigning state abbreviations currently requires "
                          "flowsa. Install via pip install "
                          "git+https://github.com/USEPA/flowsa.git#egg=flowsa")
    f = flowsa.location.get_state_FIPS(abbrev=True).drop(columns='County')
    f['State'] = f['State'].apply(lambda x: f"US-{x}")
    fd = f.set_index('FIPS').to_dict()['State']
    fd['00000'] = 'US'
    df['Location'] = df['Location'].replace(fd)
    return df.dropna(subset='Location')


def read_iso_3166():
    # accessed from the ISO online browing platform
    # https://www.iso.org/obp/ui/#search
    df = pd.read_csv(path / 'data' / 'ISO_3166.csv')
    df = df.rename(columns={'English short name': 'Name',
                            'Alpha-2 code': 'ISO-2d',
                            'Alpha-3 code': 'ISO-3d'})
    return df


if __name__ == "__main__":
    # d = extract_coordinates(group='states')
    d = extract_coordinates(group='countries')
