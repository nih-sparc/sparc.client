import os

import pytest

from sparc.client.zinchelper import ZincHelper


@pytest.fixture
def zinc():
    return ZincHelper()


def test_export_scaffold_into_vtk_format(zinc):
    # create a temporary output file
    output_location = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/"))

    # ensure the function returns None if the dataset has no Scaffold_Creator-settings.json file
    invalid_dataset_id = 1000000
    result = None
    with pytest.raises(RuntimeError):
        result = zinc.get_scaffold_as_vtk(invalid_dataset_id, output_location)
    assert result is None

    # ensure the function raises an error if the downloaded file is not scaffold_settings file
    dataset_id = 77
    with pytest.raises(AssertionError):
        zinc.get_scaffold_as_vtk(dataset_id, output_location)

    # ensure the function generates a VTK file with valid content
    dataset_id = 292
    zinc.get_scaffold_as_vtk(dataset_id, output_location)

    output_file = os.path.join(output_location, "scaffold_root.vtk")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # Clean up the temporary output file
    os.remove(output_file)


def test_export_scaffold_into_stl_format(zinc):
    # create a temporary output file
    output_location = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/"))

    # ensure the function returns None if the dataset has no Scaffold_Creator-settings.json file
    invalid_dataset_id = 1000000
    result = None
    with pytest.raises(RuntimeError):
        result = zinc.get_scaffold_as_stl(invalid_dataset_id, output_location)
    assert result is None

    # ensure the function raises an error if the downloaded file is not scaffold_settings file
    dataset_id = 77
    with pytest.raises(AssertionError):
        zinc.get_scaffold_as_stl(dataset_id, output_location)

    # ensure the function generates an STL file with valid content
    dataset_id = 292
    zinc.get_scaffold_as_stl(dataset_id, output_location)

    output_file = os.path.join(output_location, "scaffold_zinc_graphics.stl")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # Clean up the temporary output file
    os.remove(output_file)


def _mock_get_scaffold(self, dataset_id):
    self._region.readFile(os.path.join(os.path.dirname(__file__), "resources", "cube.exf"))


def test_export_scaffold_into_stl_format_non_default_coordinates(zinc):
    # create a temporary output file
    output_location = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/"))

    zinc._get_scaffold = _mock_get_scaffold.__get__(zinc)

    # ensure the function generates an STL file with valid content
    dataset_id = 292
    zinc.get_scaffold_as_stl(dataset_id, output_location)

    output_file = os.path.join(output_location, "scaffold_zinc_graphics.stl")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # Clean up the temporary output file
    os.remove(output_file)


def test_export_scaffold_into_vtk_format_with_default_output_location(zinc):
    # ensure the function generates a VTK file with valid content
    dataset_id = 292
    zinc.get_scaffold_as_vtk(dataset_id)
    assert os.path.exists("scaffold_root.vtk")
    assert os.path.getsize("scaffold_root.vtk") > 0

    # Clean up the temporary output file
    os.remove("scaffold_root.vtk")


def test_export_scaffold_into_stl_format_with_default_output_location(zinc):
    # ensure the function generates a VTK file with valid content
    dataset_id = 292
    zinc.get_scaffold_as_stl(dataset_id)

    assert os.path.exists("scaffold_zinc_graphics.stl")
    assert os.path.getsize("scaffold_zinc_graphics.stl") > 0

    # Clean up the temporary output file
    os.remove("scaffold_zinc_graphics.stl")


def test_export_mbf_to_vtk(zinc):
    # create a temporary output file
    output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/mbf_vtk.vtk"))

    # ensure the function generates a VTK file with valid content
    dataset_id = 121
    dataset_file = "11266_20181207_150054.xml"
    zinc.get_mbf_vtk(dataset_id, dataset_file, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    # Clean up the temporary output file
    os.remove(output_file)


def test_export_mbf_to_vtk_with_default_output_name(zinc):
    # ensure the function generates a VTK file with valid content
    dataset_id = 121
    dataset_file = "11266_20181207_150054.xml"
    zinc.get_mbf_vtk(dataset_id, dataset_file)
    assert os.path.exists("11266_20181207_150054.vtk")
    assert os.path.getsize("11266_20181207_150054.vtk") > 0

    # Clean up the temporary output file
    os.remove("11266_20181207_150054.vtk")


def test_analyse_with_suited_input_file(zinc):
    input_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "resources/3Dscaffold-CGRP-Mice-Dorsal-2.xml")
    )
    species = "Mice"
    organ = ["stomach", "esophagus"]
    expected = (
        f"The data file {input_file_name} is perfectly suited for mapping to the given organ."
    )
    # Call the analyse function and assert that it succeeds
    assert zinc.analyse(input_file_name, organ, species) == expected
    # Clean up the temporary output file
    os.remove(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/3Dscaffold-CGRP-Mice-Dorsal-2.exf")
        )
    )


def test_analyse_with_input_file_extra_groups(zinc):
    input_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "resources/3Dscaffold-CGRP-Mice-Dorsal-1.xml")
    )
    species = "Mice"
    organ = ["stomach", "esophagus"]
    expected = (
        f"The data file {input_file_name} "
        "is suited for mapping to the given organ. However, Axon, Blood vessel, "
        "Gastroduodenal junction, Muscle layer of cardia of stomach, Myenteric ganglia "
        "groups cannot be handled by the mapping tool yet."
    )
    # Call the analyse function and assert that it succeeds
    assert zinc.analyse(input_file_name, organ, species) == expected
    # Clean up the temporary output file
    os.remove(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "resources/3Dscaffold-CGRP-Mice-Dorsal-1.exf")
        )
    )


def test_analyse_with_input_file_without_group(zinc):
    # Test file that has no group
    input_file_name = "test_input.xml"
    organ = "stomach"
    expected = (
        f"The data file {input_file_name} doesn't have any groups, "
        f"therefore this data file is not suitable for mapping."
    )
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
