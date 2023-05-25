import os
import pytest

from sparc.client.zinchelper import ZincHelper


@pytest.fixture
def zinc():
    return ZincHelper()


def test_get_scaffold_description(zinc):
    # create a temporary output file
    output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/scaffold.vtk"))

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
    output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/mbf_vtk.vtk"))

    # ensure the function generates a VTK file with valid content
    dataset_id = 107
    dataset_file = "10991_20180817_143553.xml"
    zinc.get_mbf_vtk(dataset_id, dataset_file, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # ensure the function raises an error if the mbfxml file is malformed
    dataset_id = 287
    dataset_file = "15_1.xml"
    with pytest.raises(Exception):
        zinc.get_mbf_vtk(dataset_id, dataset_file, output_file)

    # Clean up the temporary output file
    os.remove(output_file)


def test_analyse_with_suited_input_file(zinc):
    input_file_name = "resources/3Dscaffold-CGRP-Mice-Dorsal-2.xml"
    species = "Mice"
    organ = "stomach"
    expected = "The data file resources/3Dscaffold-CGRP-Mice-Dorsal-2.xml " \
               "is perfectly suited for mapping to the given organ."
    # Call the analyse function and assert that it succeeds
    assert zinc.analyse(input_file_name, organ, species) == expected
    # Clean up the temporary output file
    os.remove("resources/3Dscaffold-CGRP-Mice-Dorsal-2.exf")


def test_analyse_with_input_file_extra_groups(zinc):
    input_file_name = "resources/3Dscaffold-CGRP-Mice-Dorsal-1.xml"
    species = "Mice"
    organ = "stomach"
    expected = "The data file resources/3Dscaffold-CGRP-Mice-Dorsal-1.xml " \
               "is suited for mapping to the given organ. However, Axon, Blood vessel, " \
               "Gastroduodenal junction, Muscle layer of cardia of stomach, Myenteric ganglia " \
               "groups cannot be handled by the mapping tool yet."
    # Call the analyse function and assert that it succeeds
    assert zinc.analyse(input_file_name, organ, species) == expected
    # Clean up the temporary output file
    os.remove("resources/3Dscaffold-CGRP-Mice-Dorsal-1.exf")


def test_analyse_with_input_file_without_group(zinc):
    # Test file that has no group
    input_file_name = "test_input.xml"
    organ = "stomach"
    expected = f"The data file {input_file_name} doesn't have any group."
    with open(input_file_name, "w") as f:
        f.write("<root><data>Test data</data></root>")
    # Call the analyse function and assert that it succeeds
    assert zinc.analyse(input_file_name, organ) == expected
    # Clean up the temporary output file
    os.remove(input_file_name)
    os.remove("test_input.exf")


def test_analyse_with_unhandled_organ(zinc):
    # Create a temporary input file for testing
    input_file_name = "resources/3Dscaffold-CGRP-Mice-Dorsal-1.xml"
    organ = "Brain"
    expected = f"The {organ.lower()} organ is not handled by the mapping tool."
    # Call the analyse function and assert that it raises an AssertionError
    assert zinc.analyse(input_file_name, organ) == expected


def test_analyse_with_invalid_input_file_type(zinc):
    # Create a temporary input file with an invalid extension
    input_file_name = "test_input.txt"
    organ = "stomach"
    with open(input_file_name, "w") as f:
        f.write("This is not an XML file")
    # Call the analyse function and assert that it raises a ValueError
    with pytest.raises(ValueError):
        zinc.analyse(input_file_name, organ)
    # Clean up the temporary file
    os.remove(input_file_name)


def test_analyse_with_invalid_input_file_content(zinc):
    # Create a temporary input file for testing
    input_file_name = "test_input.xml"
    organ = "stomach"
    with open(input_file_name, "w") as f:
        f.write("<root><data>Test data</root>")
    # Call the analyse function and assert that it raises an MBFXMLFormat
    with pytest.raises(Exception):
        zinc.analyse(input_file_name, organ)
    # Clean up the temporary input file
    os.remove(input_file_name)
