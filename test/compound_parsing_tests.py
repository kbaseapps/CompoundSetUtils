from CompoundSetUtils import compound_parsing

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
