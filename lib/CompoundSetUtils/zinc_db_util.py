import requests
from requests.exceptions import HTTPError
import logging


def _get_zinc_id(inchikey):
    url = 'http://zinc15.docking.org/substances.txt:zinc_id?inchikey=' + inchikey
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        raise ValueError(f'HTTP error occurred: {http_err}')
    except Exception as err:
        raise ValueError(f'Other error occurred: {err}')
    else:
        zinc_id = response.text.rstrip()
        print('Found ZINC ID {} for InChiKey {}'.format(zinc_id, inchikey))
        return zinc_id


def _get_mol2_text(zinc_id):
    url = 'http://zinc15.docking.org/substances/{}.mol2'.format(zinc_id)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        logging.warning('Failed to query ZINC. Error: {}'.format(http_err))
        return False
    except Exception as err:
        logging.warning('Other error occurred. Error: {}'.format(err))
        return False
    else:
        return response.text.rstrip()


def inchikey_to_mol2(inchikey, mol2_file_path):
    mol2_txt = _get_mol2_text(_get_zinc_id(inchikey))

    if mol2_txt:
        with open(mol2_file_path, 'a') as mol2_file:
            mol2_file.write(mol2_txt)
        return True
    else:
        return False
