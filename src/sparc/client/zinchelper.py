import json
import os
import re

from cmlibs.zinc.context import Context
from cmlibs.zinc.result import RESULT_OK
from cmlibs.utils.zinc.field import get_group_list
from scaffoldmaker import scaffolds
from scaffoldmaker.annotation.bladder_terms import get_bladder_term
from scaffoldmaker.annotation.body_terms import get_body_term
from scaffoldmaker.annotation.brainstem_terms import get_brainstem_term
from scaffoldmaker.annotation.colon_terms import get_colon_term
from scaffoldmaker.annotation.esophagus_terms import get_esophagus_term
from scaffoldmaker.annotation.heart_terms import get_heart_term
from scaffoldmaker.annotation.lung_terms import get_lung_term
from scaffoldmaker.annotation.muscle_terms import get_muscle_term
from scaffoldmaker.annotation.nerve_terms import get_nerve_term
from scaffoldmaker.annotation.smallintestine_terms import get_smallintestine_term
from scaffoldmaker.annotation.stellate_terms import get_stellate_term
from scaffoldmaker.annotation.stomach_terms import get_stomach_term
from scaffoldmaker.utils.exportvtk import ExportVtk
from sparc.client.services.pennsieve import PennsieveService
from mbfxml2ex.app import read_xml
from mbfxml2ex.zinc import load, write_ex


class ZincHelper:
    def __init__(self):
        self._allOrgan = {
            "bladder": get_bladder_term,
            "body": get_body_term,
            "brainstem": get_brainstem_term,
            "colon": get_colon_term,
            "esophagus": get_esophagus_term,
            "heart": get_heart_term,
            "lung": get_lung_term,
            "muscle": get_muscle_term,
            "nerve": get_nerve_term,
            "smallintestine": get_smallintestine_term,
            "stellate": get_stellate_term,
            "stomach": get_stomach_term,
        }

        self._context = Context("sparcclient")
        self._region = self._context.getDefaultRegion()
        self._pennsieveService = PennsieveService(connect=False)

    def download_files(
            self,
            limit=10,
            offset=0,
            file_type=None,
            query=None,
            organization=None,
            organization_id=None,
            dataset_id=None
    ):
        file_list = self._pennsieveService.list_files(
            limit, offset, file_type, query, organization, organization_id, dataset_id
        )
        try:
            response = self._pennsieveService.download_file(file_list=file_list)
        except Exception:
            raise RuntimeError("The dataset is not downloaded.")
        assert response.status_code == 200
        return file_list[0]["name"]

    def get_scaffold_vtk(self, dataset_id, output_file=None):
        scaffold_setting_file = self.download_files(
            limit=1,
            file_type='JSON',
            query="Scaffold_Creator-settings.json",
            dataset_id=dataset_id
        )
        with open(scaffold_setting_file) as f:
            c = json.load(f)

        assert "scaffold_settings" in c
        assert "scaffoldPackage" in c["scaffold_settings"]

        sm = scaffolds.Scaffolds_decodeJSON(c["scaffold_settings"]["scaffoldPackage"])
        sm.generate(self._region)
        ex = ExportVtk(self._region, "Scaffold VTK export.")
        if not output_file:
            output_file = "Scaffold_Creator-settings.vtk"
        ex.writeFile(output_file)
        os.remove(scaffold_setting_file)

    def get_mbf_vtk(self, dataset_id, dataset_file, output_file=None):
        segmentation_file = self.download_files(
            limit=1,
            file_type="XML",
            query=dataset_file,
            dataset_id=dataset_id
        )
        contents = read_xml(segmentation_file)
        load(self._region, contents, None)
        ex = ExportVtk(self._region, "MBF XML VTK export.")
        if not output_file:
            output_file = dataset_file.split(".")[0] + ".vtk"
        ex.writeFile(output_file)
        os.remove(segmentation_file)

    def analyse(self, input_data_file_name, organ, species=None):
        # Check input organ
        organ = organ.lower()
        if organ not in self._allOrgan:
            return f"The {organ} organ is not handled by the mapping tool."
        # Get groups from scaffoldmaker by species and organ
        get_term = self._allOrgan[organ]

        # Check if the input file is an XML file
        if not input_data_file_name.endswith(".xml"):
            raise ValueError("Input file must be a MBF XML file")

        # Read the input data file and write the contents to an ex file
        ex_file_name = os.path.splitext(input_data_file_name)[0] + ".exf"
        write_ex(ex_file_name, read_xml(input_data_file_name))

        # Read the ex file and ensure that it was loaded successfully
        result = self._region.readFile(ex_file_name)
        assert result == RESULT_OK, f"Failed to load data file {input_data_file_name}"

        # Get groups that loaded from ex file
        fieldmodule = self._region.getFieldmodule()
        groupNames = [group.getName() for group in get_group_list(fieldmodule)]
        if not groupNames:
            return f"The data file {input_data_file_name} doesn't have any group."

        regex = r"\/*([a-zA-Z]+)_*(\d+)"
        not_in_scaffoldmaker = []
        for group in groupNames:
            if group == "marker":
                continue
            matches = re.search(regex, group)
            if matches and len(matches.groups()) == 2:
                group = f"{matches.groups()[0].upper()}:{matches.groups()[1]}"
            try:
                get_term(group)
            except NameError:
                not_in_scaffoldmaker.append(group)
        if not_in_scaffoldmaker:
            return f"The data file {input_data_file_name} " \
                   f"is suited for mapping to the given organ. " \
                   f"However, {', '.join(not_in_scaffoldmaker)} groups can not handled by the mapping tool yet."
        return f"The data file {input_data_file_name} " \
               f"is perfectly suited for mapping to the given organ."
