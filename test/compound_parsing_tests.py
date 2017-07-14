from CompoundSetUtils import compound_parsing
import pickle
import os
import filecmp

comp_keys = {'dblinks', 'deltag', 'smiles', 'fingerprints', 'name', 'id',
             'charge', 'exactmass', 'deltagerr', 'inchikey', 'formula', 'mass'}


def test_read_tsv():
    compounds = compound_parsing.read_tsv('test_compounds.tsv')
    assert len(compounds) == 9
    assert not set(compounds[0].keys()) ^ comp_keys
    assert len(compounds[0]['fingerprints']) == 2


def test_read_sdf():
    compounds = compound_parsing.read_sdf('test_compounds.sdf')
    assert len(compounds) == 10
    assert not set(compounds[0].keys()) ^ (comp_keys - {'deltagerr', 'deltag'})
    assert len(compounds[0]['fingerprints']) == 2


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