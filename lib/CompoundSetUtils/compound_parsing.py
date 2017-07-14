from rdkit.Chem import AllChem, Descriptors
import os
import csv


def _make_compound_info(mol_object):
    return {
        'smiles': AllChem.MolToSmiles(mol_object, True),
        'inchikey': AllChem.InchiToInchiKey(AllChem.MolToInchi(mol_object)),
        'mass': Descriptors.MolWt(mol_object),
        'exactmass': AllChem.CalcExactMolWt(mol_object),
        'formula': AllChem.CalcMolFormula(mol_object),
        'charge': AllChem.GetFormalCharge(mol_object),
        'fingerprints': {
            'maccs': dict([(str(x), 1) for x in AllChem.GetMACCSKeysFingerprint(mol_object).GetOnBits()]),
            'rdkit': dict([(str(x), 1) for x in AllChem.RDKFingerprint(mol_object).GetOnBits()]),
        },
        'dblinks': {},
    }


def read_tsv(file_path, structure_field='structure'):
    cols_to_copy = {'name': str, 'deltag': float, 'deltagerr': float}
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    compounds = []
    w = csv.DictReader(open(file_path), dialect='excel-tab')
    for i, line in enumerate(w):
        # Generate Mol object from InChI code if present
        if "InChI=" in line[structure_field]:
            mol = AllChem.MolFromInchi(line[structure_field])
        # Otherwise generate Mol object from SMILES string
        else:
            mol = AllChem.MolFromSmiles(line[structure_field])
        if not mol:
            print("Unable to Parse %s" % line[structure_field])
            continue

        comp = {'id': '%s_%s' % (file_name, i + 1)}
        comp.update(_make_compound_info(mol))
        for col in cols_to_copy:
            if col in line:
                comp[col] = cols_to_copy[col](line[col])
        compounds.append(comp)
    return compounds


def read_sdf(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    sdf = AllChem.SDMolSupplier(file_path)
    compounds = []
    for i, mol in enumerate(sdf):
        comp = {'id': '%s_%s' %(file_name, i+1), 'name': mol.GetProp("_Name")}
        comp.update(_make_compound_info(mol))
        compounds.append(comp)
    return compounds


def parse_model(model):
    raise NotImplementedError


def write_tsv(compound_set, outfile_path):
    cols = ['id', 'name', 'smiles', 'inchikey', 'charge', 'formula', 'mass',
            'exactmass', 'compound_ref', 'modelcompound_ref', 'deltag',
            'deltagerr']
    writer = csv.DictWriter(open(outfile_path, 'w'), cols, dialect='excel-tab',
                            extrasaction='ignore')
    writer.writeheader()
    for compound in compound_set['compounds']:
        writer.writerow(compound)
    return outfile_path


def write_sdf(compound_set, outfile_path):
    no_export = {'smiles', 'fingerprints', 'dblinks'}
    writer = AllChem.SDWriter(open(outfile_path, 'w'))
    for compound in compound_set['compounds']:
        mol = AllChem.MolFromSmiles(compound['smiles'])
        for prop, val in compound.items():
            if prop in no_export:
                continue
            mol.SetProp(str(prop), str(val))
        writer.write(mol)
    return outfile_path
