# -*- coding: utf-8 -*-
import json  # noqa: F401
import os  # noqa: F401
import pickle
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ
import zipfile
import csv

from unittest.mock import patch

from CompoundSetUtils.CompoundSetUtilsImpl import CompoundSetUtils
from CompoundSetUtils.CompoundSetUtilsServer import MethodContext
from CompoundSetUtils.authclient import KBaseAuth as _KBaseAuth
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace as workspaceService


class CompoundSetUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('CompoundSetUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'CompoundSetUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = CompoundSetUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.dfu = DataFileUtil(cls.callback_url)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsId'):
            cls.wsClient.delete_workspace({'id': cls.wsId})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsId(self):
        if hasattr(self.__class__, 'wsId'):
            return self.__class__.wsId
        suffix = int(time.time() * 1000)
        wsName = "test_CompoundSetUtils_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsId = ret[0]
        return ret[0]

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @staticmethod
    def fake_staging_download(params):
        scratch = '/kb/module/work/tmp/'
        inpath = params['staging_file_subdir_path']
        shutil.copy('/kb/module/test/'+inpath, scratch+inpath)
        return {'copy_file_path': scratch+inpath}

    def save_compound_set(self):
        comp_set = pickle.load(open('/kb/module/test/compound_set.pkl', 'rb'))
        ws_obj = {"type": "KBaseBiochem.CompoundSet", "data": comp_set,
                  "name": comp_set['name']}
        info = self.getWsClient().save_objects({'id': self.getWsId(),
                                                "objects": [ws_obj]})[0]
        compoundset_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        return compoundset_ref

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_from_file_tsv(self):
        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'tsv_set',
                  'mol2_staging_file_path': 'mol2_files_missing_comp.zip'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        assert ret and ('report_name' in ret)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_from_exported_tsv(self):
        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_out.tsv',
                  'compound_set_name': 'tsv_set_2'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        assert ret and ('report_name' in ret)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_from_file_sdf(self):
        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.sdf',
                  'compound_set_name': 'sdf_set',
                  'mol2_staging_file_path': 'mol2_files.zip'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        assert ret and ('report_name' in ret)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_to_file_tsv(self):

        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'tsv_set',
                  'mol2_staging_file_path': 'mol2_files.zip'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        compoundset_ref = ret['compoundset_ref']
        params = {'compound_set_ref': compoundset_ref,
                  'output_format': 'tsv'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret) and ('packed_mol2_files_path' in ret) and ('comp_id_mol2_file_name_map' in ret)

        print('compound_set_from_file output\n{}\n'.format(ret))

        mol2_file_path = ret['packed_mol2_files_path']

        mol2_files = zipfile.ZipFile(mol2_file_path).namelist()
        mol2_file_names = [os.path.splitext(os.path.basename(mol2_file))[0] for mol2_file in mol2_files]

        w = csv.DictReader(open('test_compounds.tsv'), dialect='excel-tab')

        comp_ids = []
        for line in w:
            comp_ids.append(line.get('id'))

        self.assertCountEqual(mol2_file_names, comp_ids)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_mol2_files_to_pdbqt(self):

        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'tsv_set',
                  'mol2_staging_file_path': 'mol2_files_missing_comp.zip'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        params = {'input_ref': ret['compoundset_ref']}
        ret = self.getImpl().convert_compoundset_mol2_files_to_pdbqt(self.getContext(), params)[0]
        assert ret and ('packed_pdbqt_files_path' in ret) and ('comp_id_pdbqt_file_name_map' in ret)

        pdbqt_file_path = ret['packed_pdbqt_files_path']

        pdbqt_files = zipfile.ZipFile(pdbqt_file_path).namelist()
        pdbqt_file_names = [os.path.splitext(os.path.basename(pdbqt_file))[0] for pdbqt_file in pdbqt_files]

        w = csv.DictReader(open('test_compounds.tsv'), dialect='excel-tab')

        comp_ids = []
        for line in w:
            comp_ids.append(line.get('id'))

        self.assertEqual(len(comp_ids) - 1, len(pdbqt_file_names))
        self.assertTrue(set(pdbqt_file_names).issubset(comp_ids))

    def test_compound_set_to_file_sdf(self):
        compoundset_ref = self.save_compound_set()
        params = {'compound_set_ref': compoundset_ref,
                  'output_format': 'sdf'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret)

    def test_compound_set_to_file_mol(self):
        compoundset_ref = self.save_compound_set()
        params = {'compound_set_ref': compoundset_ref,
                  'output_format': 'mol'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret)

    def test_compound_set_to_file_pdb(self):
        compoundset_ref = self.save_compound_set()
        params = {'compound_set_ref': compoundset_ref,
                  'output_format': 'pdb'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret)

    def test_compound_set_to_file_bad_input(self):
        compoundset_ref = self.save_compound_set()
        with self.assertRaisesRegex(ValueError, 'parameter is required'):
            self.getImpl().compound_set_to_file(self.getContext(),
                                                {'compound_set_ref': compoundset_ref})

        with self.assertRaisesRegex(ValueError, 'parameter is required'):
            self.getImpl().compound_set_to_file(self.getContext(),
                                                {'output_format': 'pdb'})

    def test_compound_set_from_model(self):
        model = json.load(open('/kb/module/test/iMR1_799.json'))
        ws_obj = {"type": "KBaseFBA.FBAModel", "data": model,
                  "name": model['name']}
        info = self.getWsClient().save_objects({'id': self.getWsId(),
                                                "objects": [ws_obj]})[0]
        model_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        params = {'workspace_id': self.getWsId(),
                  'model_ref': model_ref,
                  'compound_set_name': 'model_set'}
        ret = self.getImpl().compound_set_from_model(self.getContext(), params)[0]
        assert ret and ('report_name' in ret)

    def test_compound_set_export(self):
        compoundset_ref = self.save_compound_set()
        ret1 = self.getImpl().export_compoundset_as_tsv(
            self.getContext(), {'input_ref': compoundset_ref})[0]['shock_id']
        assert ret1 and ret1.count('-') == 4
        ret2 = self.getImpl().export_compoundset_as_sdf(
            self.getContext(), {'input_ref': compoundset_ref})[0]['shock_id']
        assert ret2 and ret2.count('-') == 4

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_mol2_export(self):
        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'tsv_set',
                  'mol2_staging_file_path': 'mol2_files.zip'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]

        mol2_file = self.getImpl().export_compoundset_mol2_files(
                                    self.getContext(),
                                    {'input_ref': ret['compoundset_ref']})[0]['packed_mol2_files_path']

        mol2_files = zipfile.ZipFile(mol2_file).namelist()
        mol2_file_names = [os.path.splitext(os.path.basename(mol2_file))[0] for mol2_file in mol2_files]

        w = csv.DictReader(open('test_compounds.tsv'), dialect='excel-tab')

        comp_ids = []
        for line in w:
            comp_ids.append(line.get('id'))

        self.assertCountEqual(mol2_file_names, comp_ids)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_fetch_mol2_from_zinc(self):
        params = {'workspace_id': self.getWsId(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'tsv_set'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)[0]
        compoundset_ref = ret['compoundset_ref']

        compoundset = self.dfu.get_objects(
                                {'object_refs': [compoundset_ref]})['data'][0]['data']
        hids = [comp.get('mol2_handle_ref') for comp in compoundset['compounds']]

        self.assertCountEqual(hids, [None]*9)

        params = {'workspace_id': self.getWsId(),
                  'compoundset_ref': compoundset_ref}
        new_compoundset_ref = self.getImpl().fetch_mol2_files_from_zinc(
                                            self.getContext(), params)[0]['compoundset_ref']
        new_compoundset = self.dfu.get_objects(
                                {'object_refs': [new_compoundset_ref]})['data'][0]['data']
        new_hids = [comp.get('mol2_handle_ref') for comp in new_compoundset['compounds']]

        self.assertTrue(new_hids.count(None) < 9)
