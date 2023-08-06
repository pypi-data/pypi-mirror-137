from test_all import test_function
from geoformat.driver.csv_driver import csv_to_geolayer
from pathlib import Path

from tests.data.geolayers import geolayer_paris_velib, geolayer_paris_velib_str

file_path_base = Path(__file__).parent.parent.parent.parent.joinpath

csv_to_geolayer_parameters = {
    0: {
        "path": file_path_base('data/csv/velib-disponibilite-en-temps-reel.csv'),
        "delimiter": ';',
        "header": True,
        "field_name_filter": None,
        "force_field_conversion": False,
        "serialize": False,
        "return_value": geolayer_paris_velib_str
    },
    1: {
        "path": file_path_base('data/csv/velib-disponibilite-en-temps-reel.csv'),
        "delimiter": ';',
        "header": True,
        "field_name_filter": None,
        "force_field_conversion": True,
        "serialize": False,
        "return_value": geolayer_paris_velib
    }
}

def test_all():


    # csv_to_geolayer
    print(test_function(csv_to_geolayer, csv_to_geolayer_parameters))

if __name__ == '__main__':
    test_all()