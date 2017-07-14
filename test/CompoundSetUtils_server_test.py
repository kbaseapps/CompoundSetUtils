# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from CompoundSetUtils.CompoundSetUtilsImpl import CompoundSetUtils
from CompoundSetUtils.CompoundSetUtilsServer import MethodContext
from CompoundSetUtils.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from mock import patch
import shutil
import pickle


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
        print(cls.scratch)
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_CompoundSetUtils_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

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
        info = self.getWsClient().save_objects({'workspace': self.getWsName(),
                                                "objects": [ws_obj]})[0]
        return comp_set['name']

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_from_file_tsv(self):
        params = {'workspace_name': self.getWsName(),
                  'staging_file_path': 'test_compounds.tsv',
                  'compound_set_name': 'sdf_set'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)

    @patch.object(DataFileUtil, "download_staging_file",
                  new=fake_staging_download)
    def test_compound_set_from_file_sdf(self):
        params = {'workspace_name': self.getWsName(),
                  'staging_file_path': 'test_compounds.sdf',
                  'compound_set_name': 'sdf_set'}
        ret = self.getImpl().compound_set_from_file(self.getContext(), params)

    def test_compound_set_to_file_tsv(self):
        compoundset_ref = self.save_compound_set()
        params = {'workspace_name': self.getWsName(),
                  'compound_set_name': compoundset_ref,
                  'output_format': 'tsv'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)

    def test_compound_set_to_file_sdf(self):
        compoundset_ref = self.save_compound_set()
        params = {'workspace_name': self.getWsName(),
                  'compound_set_name': compoundset_ref,
                  'output_format': 'sdf'}
        ret = self.getImpl().compound_set_to_file(self.getContext(), params)

    def test_compound_set_from_model(self):
        model = json.load(open('/kb/module/test/iMR1_799.json'))
        ws_obj = {"type": "KBaseFBA.FBAModel", "data": model,
                  "name": model['name']}
        info = self.getWsClient().save_objects({'workspace': self.getWsName(),
                                                "objects": [ws_obj]})[0]
        params = {'workspace_name': self.getWsName(),
                  'model_name': model['name'],
                  'compound_set_name': 'model_set'}
        ret = self.getImpl().compound_set_from_model(self.getContext(), params)
