import csv

import geoformat
from geoformat.conf.path import verify_input_path_is_file
from geoformat.conversion.feature_conversion import feature_list_to_geolayer


def _from_csv_get_features_list(csv_reader, header):
    """
    Take csv reader object and yield csv row into geoformat feature

    :param csv_reader: csv reader object.
    :param header: Specifies that the file contains a header line with the names of each column in the file. (bool)

    :return: geoformat Feature
    """
    for i_row, row in enumerate(csv_reader):
        if i_row == 0:
            if header is True:
                field_name_list = list(row)
                continue
            else:
                field_name_list = ['field_{}'.format(i_field) for i_field in range(len(row))]

        feature = {}
        feature['attributes'] = {field_name: row[i_field] for i_field, field_name in enumerate(field_name_list)}
        yield feature


def csv_to_geolayer(
        path,
        delimiter=',',
        header=True,
        field_name_filter=None,
        force_field_conversion=False,
        serialize=False,
):
    """
    From csv file get a geolayer.

    :param path: path to csv file
    :param delimiter: Specifies the character that separates columns within each row (line) of the file.
     The default is comma character.
    :param header: Specifies that the file contains a header line with the names of each column in the file. (bool)
    :param field_name_filter: filter only on specified field_name (can be a list)
    :param force_field_conversion: True if you want to force value in field (can change field type) / False if you want
           to deduce field type without forcing field type.
    :param serialize: True if features in geolayer are serialized (can reduce performance) / False if not.

    :return: geolayer
    """
    # verify that path exist
    p = verify_input_path_is_file(path)

    with open(p, 'r') as csv_file:
        raw_feature_list = csv.reader(csv_file, delimiter=delimiter)

        raw_feature_list = list(_from_csv_get_features_list(csv_reader=raw_feature_list, header=header))

        geolayer = feature_list_to_geolayer(
            feature_list=raw_feature_list,
            geolayer_name=p.stem,
            field_name_filter=field_name_filter,
            force_field_conversion=force_field_conversion,
            crs=None,
            serialize=serialize
        )

        return geolayer
