import filecmp
import json
import os
import pickle
import unittest

from CompoundSetUtils import compound_parsing

comp_keys = {'dblinks', 'deltag', 'smiles', 'fingerprints', 'name', 'id', 'mol',
             'charge', 'exactmass', 'deltagerr', 'inchikey', 'formula', 'mass'}

class CompoundParseingTest(unittest.TestCase):
    def test_read_tsv(self):
        compounds = compound_parsing.read_tsv('test_compounds.tsv', 'structure',
                                              '../data/Inchikey_IDs.json')
        self.assertEqual(len(compounds), 9)
        self.assertCountEqual(compounds[0].keys(), comp_keys - {'mol'})
        self.assertEqual(len(compounds[0]['fingerprints']), 2)
        self.assertEqual(compounds[2]['id'],'cpd00939')

    def test_read_sdf(self):
        compounds = compound_parsing.read_sdf('test_compounds.sdf', '../data/Inchikey_IDs.json')
        self.assertEqual(len(compounds), 10)
        self.assertCountEqual(compounds[0].keys(), comp_keys - {'deltagerr', 'deltag'})
        assert len(compounds[0]['fingerprints']) == 2
        assert 'mol' in compounds[0]

    def test_parse_model(self):
        model = json.load(open('iMR1_799.json'))
        compounds, undefined = compound_parsing.parse_model(model, '../data/Compound_Structures.json')
        self.assertEqual(len(compounds), 424)
        self.assertEqual(len(undefined), 321)
        self.assertEqual(compounds[0]['id'], 'cpd01892')
        self.assertEqual(undefined[0], 'cpd11493')

    def test_write_tsv(self):
        expected_file = 'test.tsv'
        try:
            compound_set = pickle.load(open('compound_set.pkl', 'rb'))
            file_path = compound_parsing.write_tsv(compound_set, expected_file)
            filecmp.cmp(file_path, 'test_out.tsv')
        finally:
            if os.path.exists(expected_file):
                os.remove(expected_file)

    def test_write_sdf(self):
        expected_file = 'test.sdf'
        try:
            compound_set = pickle.load(open('compound_set.pkl', 'rb'))
            file_path = compound_parsing.write_sdf(compound_set, expected_file)
            filecmp.cmp(file_path, 'test_out.sdf')
        finally:
            if os.path.exists(expected_file):
                os.remove(expected_file)