# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid

import CompoundSetUtils.compound_parsing as parse
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class CompoundSetUtils:
    '''
    Module Name:
    CompoundSetUtils

    Module Description:
    A KBase module: CompoundSetUtils
Contains tools for import & export of compound sets
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "2.0.0"
    GIT_URL = "git@github.com:kbaseapps/CompoundSetUtils.git"
    GIT_COMMIT_HASH = "fe9839c7b2a6371babb0b017f23a9f3ad41aa5b9"

    #BEGIN_CLASS_HEADER
    @staticmethod
    def _check_param(in_params, req_param, opt_param=list()):
        """
        Check if each of the params in the list are in the input params
        """
        for param in req_param:
            if param not in in_params:
                raise ValueError('{} parameter is required'.format(param))
        defined_param = set(req_param+opt_param)
        for param in in_params:
            if param not in defined_param:
                logging.warning("Received unexpected parameter {}".format(param))

    def _save_to_ws_and_report(self, ws_id, source, compoundset):
        """Save compound set to the workspace and make report"""
        info = self.dfu.save_objects(
            {'id': ws_id,
             "objects": [{
                 "type": "KBaseBiochem.CompoundSet",
                 "data": compoundset,
                 "name": compoundset['name']
             }]})[0]
        compoundset_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        report_params = {
            'objects_created': [{'ref': compoundset_ref,
                                 'description': 'Compound Set'}],
            'message': 'Imported %s as %s' % (source, info[1]),
            'workspace_name': info[7],
            'report_object_name': 'compound_set_creation_report'
        }

        # Construct the output to send back
        report_client = KBaseReport(self.callback_url)
        report_info = report_client.create_extended_report(report_params)
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref'],
                  'compoundset_ref': compoundset_ref}
        return output

    def _export_compound_set(self, ref, file_type):
        logging.info("Exporting {} as {}".format(ref, file_type))
        compoundset = self.dfu.get_objects(
            {'object_refs': [ref]}
        )['data'][0]['data']
        temp_dir = "{}/{}".format(self.scratch, uuid.uuid4())
        os.mkdir(temp_dir)
        out_dir = "{}/{}".format(temp_dir, compoundset['name'])
        os.mkdir(out_dir)
        target = "{}/{}.{}".format(out_dir, compoundset['name'], file_type)
        if file_type == 'tsv':
            parse.write_tsv(compoundset, target)
        elif file_type == 'sdf':
            parse.write_sdf(compoundset, target)
        else:
            raise ValueError("Bad file_type: {}".format(file_type))
        handle = self.dfu.package_for_download(
            {'file_path': out_dir, 'ws_refs': [ref]})
        output = {'shock_id': handle['shock_id']}
        return output
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        #END_CONSTRUCTOR
        pass


    def compound_set_from_file(self, ctx, params):
        """
        CompoundSetFromFile
        string staging_file_path
        :param params: instance of type "compoundset_upload_params" ->
           structure: parameter "workspace_id" of String, parameter
           "staging_file_path" of String, parameter "compound_set_name" of
           String
        :returns: instance of type "compoundset_upload_results" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "compoundset_ref" of type "obj_ref"
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN compound_set_from_file
        self._check_param(params, ['workspace_id', 'staging_file_path',
                                   'compound_set_name'])
        scratch_file_path = self.dfu.download_staging_file(
            {'staging_file_subdir_path': params['staging_file_path']}
        ).get('copy_file_path')
        # I probably should be uploading the raw files to shock

        ext = os.path.splitext(scratch_file_path)[1]
        file_name = os.path.basename(scratch_file_path)
        if ext == '.sdf':
            compounds = parse.read_sdf(scratch_file_path)
        elif ext == '.tsv':
            compounds = parse.read_tsv(scratch_file_path)
        else:
            raise ValueError('Invalid input file type. Expects .tsv or .sdf')

        compoundset = {
            'id': params['compound_set_name'],
            'name': params['compound_set_name'],
            'description': 'Compound Set produced from %s' % file_name,
            'compounds': compounds,
        }

        output = self._save_to_ws_and_report(params['workspace_id'],
                                             params['staging_file_path'],
                                             compoundset)
        #END compound_set_from_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method compound_set_from_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def compound_set_to_file(self, ctx, params):
        """
        CompoundSetToFile
        string compound_set_name
        string output_format
        :param params: instance of type "compoundset_download_params" ->
           structure: parameter "compound_set_ref" of String, parameter
           "output_format" of String
        :returns: instance of type "compoundset_download_results" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN compound_set_to_file
        self._check_param(params, ['compound_set_ref', 'output_format'])
        ret = self.dfu.get_objects(
            {'object_refs': [params['compound_set_ref']]}
        )['data'][0]
        workspace_name = ret['info'][7]
        compoundset = ret['data']
        ext = params['output_format']
        out = "%s/%s.%s" % (self.scratch, compoundset['name'], ext)
        if ext == 'sdf':
            outfile_path = parse.write_sdf(compoundset, out)
        elif ext == 'tsv':
            outfile_path = parse.write_tsv(compoundset, out)
        else:
            raise ValueError('Invalid output file type. Expects tsv or sdf')

        report_files = [{'path': outfile_path,
                         'name': os.path.basename(outfile_path),
                         'label': os.path.basename(outfile_path),
                         'description': 'A compound set in %s format' % ext}]

        report_params = {
            'message': 'Converted %s compound set to %s format.' % (
                compoundset['name'], params['output_format']),
            'file_links': report_files,
            'workspace_name': workspace_name,
            'report_object_name': 'compound_set_download_report'
        }

        # Construct the output to send back
        report_client = KBaseReport(self.callback_url)
        report_info = report_client.create_extended_report(report_params)
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']}
        #END compound_set_to_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method compound_set_to_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def compound_set_from_model(self, ctx, params):
        """
        CompoundSetFromModel
        required:
        string workspace_id
        string model_ref
        string compound_set_name
        :param params: instance of type "compoundset_from_model_params" ->
           structure: parameter "workspace_id" of String, parameter
           "model_ref" of String, parameter "compound_set_name" of String
        :returns: instance of type "compoundset_upload_results" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "compoundset_ref" of type "obj_ref"
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN compound_set_from_model
        self._check_param(params, ['workspace_id', 'model_ref',
                                   'compound_set_name'])
        model = self.dfu.get_objects(
            {'object_refs': [params['model_ref']]}
        )['data'][0]['data']
        compounds, undef = parse.parse_model(model)
        compoundset = {
            'id': params['compound_set_name'],
            'name': params['compound_set_name'],
            'description': 'Compound Set produced from %s, a metabolic model'
                           % model['id'],
            'compounds': compounds,
        }

        output = self._save_to_ws_and_report(params['workspace_id'],
                                             model['name'], compoundset)
        #END compound_set_from_model

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method compound_set_from_model return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_compoundset_as_tsv(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_compoundset_as_tsv
        output = self._export_compound_set(params['input_ref'], 'tsv')
        #END export_compoundset_as_tsv

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_compoundset_as_tsv return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_compoundset_as_sdf(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_compoundset_as_sdf
        output = self._export_compound_set(params['input_ref'], 'sdf')
        #END export_compoundset_as_sdf

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_compoundset_as_sdf return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
