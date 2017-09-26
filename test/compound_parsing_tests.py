from CompoundSetUtils import compound_parsing
import pickle
import json
import os
import filecmp

comp_keys = {'dblinks', 'deltag', 'smiles', 'fingerprints', 'name', 'id',
             'charge', 'exactmass', 'deltagerr', 'inchikey', 'formula', 'mass'}


def test_read_tsv():
    compounds = compound_parsing.read_tsv('test_compounds.tsv', 'structure',
                                          '../data/Inchikey_IDs.json')
    assert len(compounds) == 9
    assert not set(compounds[0].keys()) ^ comp_keys
    assert len(compounds[0]['fingerprints']) == 2
    assert compounds[2]['id'] == 'cpd00939'
    print(compounds)


def test_read_sdf():
    compounds = compound_parsing.read_sdf('test_compounds.sdf', '../data/Inchikey_IDs.json')
    assert len(compounds) == 10
    assert not set(compounds[0].keys()) ^ (comp_keys - {'deltagerr', 'deltag'})
    assert len(compounds[0]['fingerprints']) == 2


def test_parse_model():
    model = json.load(open('iMR1_799.json'))
    compounds, undefined = compound_parsing.parse_model(model, '../data/Compound_Structures.json')
    assert len(compounds) == 424
    assert len(undefined) == 321
    assert compounds[0]['id'] == 'cpd01892'
    assert undefined[0] == 'cpd11493'


def test_write_tsv():
    expected_file = 'test.tsv'
    try:
        compound_set = pickle.load(open('compound_set.pkl', 'rb'))
        file_path = compound_parsing.write_tsv(compound_set, expected_file)
        filecmp.cmp(file_path, 'test_out.tsv')
    finally:
        if os.path.exists(expected_file):
            os.remove(expected_file)


def test_write_sdf():
    expected_file = 'test.sdf'
    try:
        compound_set = pickle.load(open('compound_set.pkl', 'rb'))
        file_path = compound_parsing.write_sdf(compound_set, expected_file)
        filecmp.cmp(file_path, 'test_out.sdf')
    finally:
        if os.path.exists(expected_file):
            os.remove(expected_file)