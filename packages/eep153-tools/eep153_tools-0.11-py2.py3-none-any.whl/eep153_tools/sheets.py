import gnupg
import os
import json
from pathlib import Path

def decrypt_credentials(encrypted_key_file,destination=os.path.expanduser('~')+'/.eep153.service_accounts/'):
    """
    Decrypt service account credentials to file in directory =destination=.
    """
    gpg = gnupg.GPG()
    passphrase = input('Input secret passphrase for %s to create google drive credentials: ' % encrypted_key_file)
    with open(encrypted_key_file,'rb') as f:
        status = gpg.decrypt_file(f,passphrase=passphrase)
        if not status.ok:
            if 'decryption failed' in status.status:
                raise ValueError('Decryption failed.  Check passphrase?')
            elif 'gpg: error' in status.stderr:
                raise IOError('Unable to write key file.')
            else:
                print('status: ',status.status)
                print('error: ',status.stderr)
                raise RuntimeError('Unable to create decrypted file.')
        else:
            acct = json.loads(status.data)
            fn = acct['client_email']
            Path(destination).mkdir(exist_ok=True) # Create path if it doesn't exist
            with open(destination +'/'+ fn,'w') as f:
                json.dump(acct,f)

def get_credentials(fn=os.path.expanduser('~')+'/.eep153.service_accounts/',encrypted_key_file='students.json.gpg'):
    """
    Load service account credentials from json file =fn=.

    If fn doesn't exist, try to create by decrypting =encrypted_key_file=.
    """
    Creds = {}
    try:
        if Path(fn).is_dir():
            key_files = os.listdir(fn)
            if len(key_files):
                for key_file in key_files:
                    Creds[key_file] = get_credentials(fn=os.path.abspath(fn+'/'+key_file),encrypted_key_file=encrypted_key_file)[key_file]
            else: raise IOError
        else:
            with open(fn) as f:
                service_account_info = json.load(f)
                Creds[service_account_info['client_email']] = service_account_info
                print('Key available for {client_email}.'.format(**service_account_info))

        return Creds

    except IOError:
        decrypt_credentials(encrypted_key_file,fn)
        return get_credentials(fn=fn,encrypted_key_file=encrypted_key_file)

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import warnings
from gspread.exceptions import APIError

def read_public_sheet(key,sheet=None):
    """
    Read a public google sheet, return as a pd.DataFrame.
    """
    # Can't use gspread
    # The below adapted from Gianmario Spacagna's suggestion at
    # https://stackoverflow.com/questions/19611729/getting-google-spreadsheet-csv-into-a-pandas-dataframe
    if 'https://' in key[:9]: # Have a url, extract key
        t = key.split('/')
        key = t[t.index('d')+1]

    url = 'https://docs.google.com/spreadsheets/d/{key}/export?format=csv'.format(key=key)
    print(url)

    if sheet is not None:
        url = url + '&gid={sheet}'.format(sheet=sheet.replace(' ', '%20'))
        print(url)
    try:
        df = pd.read_csv(url)
    except HTTPError: 
        raise HTTPError("Not found.  Check permissions?")

    return df.drop([col for col in df.columns if col.startswith('Unnamed')], axis=1)

def read_sheets(key,json_creds=None,sheet=None,force_numeric=True):
    """Read google sheet having key/url 'key'.  

    If sheet is not public, supply a =json= filename for "service
    account" credentials (see
    https://gspread.readthedocs.io/en/latest/oauth2.html).

    Final argument identifies a particular "sheet" in the "workbook".
    This can be an integer or a string.
    
    Ethan Ligon                                         January 2020

    """

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    GC = {}

    try: # key may be dict indexed by sheet
        key = key[sheet]
    except TypeError: # not a dict?
        pass

    if json_creds is not None:
        creds = Credentials.from_service_account_file(json_creds,scopes=scope)
        GC[creds.service_account_email] = gspread.authorize(creds)
    else:  # Look for existing json_creds
        try:
            json_info = get_credentials()
            for k,v in json_info.items():
                creds = Credentials.from_service_account_info(v,scopes=scope)
                GC[creds.service_account_email] = gspread.authorize(creds)
        except:
            warnings.warn('Unable to access credentials.  Trying without...')
            return read_public_sheet(key,sheet)

    if not len(GC): 
        raise RuntimeError("No valid credentials found.")

    for gc in GC.values():
        try:
            if 'https://' in key[:9]:
                wkb = gc.open_by_url(key)
            else:
                wkb = gc.open_by_key(key)
            wkb.worksheets()
            break # Once we succeed with gc, no need to try other credentials
        except APIError:
            pass # try with next creds

    try: # Did we get access?
        wkb.worksheets()
    except APIError:
        raise RuntimeError('Unable to open %s with available credentials' % key)
            

    if sheet is None:
        wks = wkb.worksheets()
        D={}
        for w in wks:
            data = w.get_all_values()
            headers = data.pop(0)
            df = pd.DataFrame(data, columns=headers)
            if force_numeric:
                D[w.title]=df.apply(lambda x: pd.to_numeric(x,errors='ignore'))
            else:
                D[w.title]=df

        return D
    else: 
        try:
            wks = wkb.get_worksheet(int(sheet))
        except ValueError:
            wks = wkb.worksheet(sheet)
            data = wks.get_all_values()
            headers = data.pop(0)
            df = pd.DataFrame(data, columns=headers)

        if force_numeric:
            return df.apply(lambda x: pd.to_numeric(x,errors='ignore'))
        else:
            return df

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from gspread_pandas import Client, Spread
from gspread_pandas.client import SpreadsheetNotFound

def write_sheet(df,user_email,user_role='reader',json_creds=None,key='',sheet='My Sheet'):
    """Write df to google sheet having =key= and sheet name =sheet=.
 
    Alternatively, key may be a title for the spreadsheet.

    If sheet is not public, supply a =json= filename for "service
    account" credentials (see
    https://gspread.readthedocs.io/en/latest/oauth2.html).

    Final argument identifies a particular "sheet" in the "workbook".
    This can be an integer or a string.
 
    Ethan Ligon                                         April 2021
    """

    if "http" in key and "/" in key: # Deal with case of a url
        url = key
        bits = url.split('/')
        key = bits[bits.index('d')+1]

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    if json_creds is not None:
        credentials = Credentials.from_service_account_file(json_creds,scopes=scope)
        gc = gspread.authorize(credentials)
    else:  # Look for existing json_creds
        json_info = get_credentials()
        credentials = Credentials.from_service_account_info(json_info,scopes=scope)
        gc = gspread.authorize(credentials)

    try:
        spread = Spread(key,creds=credentials)
        id = key
    except SpreadsheetNotFound:
        s = client.create(key)
        id = s.id
        spread = Spread(id,client=client)
        spread.delete_sheet('Sheet1')

    client.insert_permission(id,user_email,perm_type='user',role=user_role)

    spread.df_to_sheet(df,sheet=sheet)        

    return id
