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


def write_tsv(compound_set):
    raise NotImplementedError


def write_sdf(compound_set):
    raise NotImplementedError