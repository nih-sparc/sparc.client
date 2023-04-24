import json
import os

from src.sparc.client.services.pennsieve import PennsieveService
from scaffoldmaker import scaffolds
from opencmiss.zinc.context import Context
from mbfxml2ex.app import read_xml
from mbfxml2ex.zinc import load
from scaffoldmaker.utils.exportvtk import ExportVtk
from opencmiss.zinc.result import RESULT_OK

class ZincHelper:

    def __init__(self):
        self._context = Context('sparcclient')
        self._region = self._context.getDefaultRegion()
        self._pennsieveService = PennsieveService(connect=False)

    def download_files(self, limit=10, offset=0, file_type=None, query=None, organization=None, organization_id=None, dataset_id=None):
        file_list = self._pennsieveService.list_files(limit, offset, file_type, query, organization, organization_id, dataset_id)
        response = self._pennsieveService.download_file(file_list=file_list)
        assert response.status_code == 200
        return file_list[0]['name']

    def get_scaffold_vtk(self, dataset_id, output):
        scaffold_setting_file = self.download_files(limit=1, file_type='JSON', query="Scaffold_Creator-settings.json", dataset_id=dataset_id)
        with open(scaffold_setting_file) as f:
            c = json.load(f)

        assert 'scaffold_settings' in c
        assert 'scaffoldPackage' in c['scaffold_settings']

        sm = scaffolds.Scaffolds_decodeJSON(c['scaffold_settings']['scaffoldPackage'])
        sm.generate(self._region)
        ex = ExportVtk(self._region, 'Scaffold VTK export.')
        ex.writeFile(output)

    def get_mbf_vtk(self, dataset_id, output):
        segmentation_file = self.download_files(limit=1, file_type='XML', dataset_id=dataset_id)
        contents = read_xml(segmentation_file)
        load(self._region, contents, None)
        ex = ExportVtk(self._region, 'MBF XML VTK export.')
        ex.writeFile(output)

    def analyse(self, inputDataFileName):
        result = self._region.readFile(inputDataFileName)
        assert result == RESULT_OK, "Failed to load data file " + str(inputDataFileName)
