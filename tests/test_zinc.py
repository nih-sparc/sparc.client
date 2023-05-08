import os
import pytest
import json

import mbfxml2ex
from src.sparc.client.zinchelper import ZincHelper


@pytest.fixture
def zinc():
    return ZincHelper()


def test_get_scaffold_description(zinc):
    # create a temporary output file
    output_file = "files/scaffold.vtk"

    # ensure the function returns None if the dataset has no Scaffold_Creator-settings.json file
    invalid_dataset_id = 1000000
    result = None
    with pytest.raises(RuntimeError):
        result = zinc.get_scaffold_vtk(invalid_dataset_id, output_file)
    assert result is None

    # ensure the function raises an error if the downloaded file is not scaffold_settings file
    dataset_id = 77
    with pytest.raises(AssertionError):
        zinc.get_scaffold_vtk(dataset_id, output_file)

    # ensure the function generates a VTK file with valid content
    dataset_id = 292
    zinc.get_scaffold_vtk(dataset_id, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # Clean up the temporary output file
    os.remove(output_file)


def test_export_mbf_to_vtk(zinc):
    # create a temporary output file
    output_file = "files/mbf_vtk.vtk"

    # ensure the function generates a VTK file with valid content
    dataset_id = 107
    zinc.get_mbf_vtk(dataset_id, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # ensure the function raises an error if the mbfxml file is malformed
    dataset_id = 287
    with pytest.raises(mbfxml2ex.exceptions.MBFXMLFormat):
        zinc.get_mbf_vtk(dataset_id, output_file)

    # Clean up the temporary output file
    os.remove(output_file)


def test_analyse_with_valid_input_file(zinc):
    input_file_name = '10909_20180614_150758.xml'
    species = "Mice"
    organ = "stomach"
    # Call the analyse function and assert that it succeeds
    zinc.analyse(input_file_name, species, organ)
    assert os.path.isfile('10909_20180614_150758.exf')
    # Clean up the temporary output file
    os.remove('10909_20180614_150758.exf')


def test_analyse_with_invalid_input_file(zinc):
    # Test file that has group not in scaffoldmaker
    input_file_name = 'files/3D_scaffold_-_CGRP-Mice-Dorsal-3.xml'
    species = "Mice"
    organ = "stomach"
    # Call the analyse function and assert that it succeeds
    with pytest.raises(NameError):
        zinc.analyse(input_file_name, species, organ)
    assert os.path.isfile('files/3D_scaffold_-_CGRP-Mice-Dorsal-3.exf')
    # Clean up the temporary output file
    os.remove('files/3D_scaffold_-_CGRP-Mice-Dorsal-3.exf')


def test_analyse_with_no_group_input_file(zinc):
    # Test file that has no group
    input_file_name = 'files/11266_20181207_150054.xml'
    # Call the analyse function and assert that it succeeds
    with pytest.raises(AssertionError):
        zinc.analyse(input_file_name)
    assert os.path.isfile('files/11266_20181207_150054.exf')
    # Clean up the temporary output file
    os.remove('files/11266_20181207_150054.exf')


def test_analyse_with_input_file_not_suit(zinc):
    # Create a temporary input file for testing
    input_file_name = 'test_input.xml'
    with open(input_file_name, 'w') as f:
        f.write('<root><data>Test data</data></root>')
    # Call the analyse function and assert that it raises an AssertionError
    with pytest.raises(AssertionError):
        zinc.analyse(input_file_name)
    # Clean up the temporary input file
    os.remove(input_file_name)


def test_analyse_with_invalid_input_file_type(zinc):
    # Create a temporary input file with an invalid extension
    input_file_name = 'test_input.txt'
    with open(input_file_name, 'w') as f:
        f.write('This is not an XML file')
    # Call the analyse function and assert that it raises a ValueError
    with pytest.raises(ValueError):
        zinc.analyse(input_file_name)
    # Clean up the temporary file
    os.remove(input_file_name)


def test_analyse_with_invalid_input_file_content(zinc):
    # Create a temporary input file for testing
    input_file_name = 'test_input.xml'
    with open(input_file_name, 'w') as f:
        f.write('<root><data>Test data</root>')
    # Call the analyse function and assert that it raises an MBFXMLFormat
    with pytest.raises(mbfxml2ex.exceptions.MBFXMLFormat):
        zinc.analyse(input_file_name)
    # Clean up the temporary input file
    os.remove(input_file_name)
