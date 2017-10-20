from dateutil.parser import parse
import pandas as pd
import os.path
import string
import difflib

DATA_FILE_POSTCODES='../data/Postcodes.csv'

def isDate(val):
    try:
        return True, parse(val, dayfirst=True)
    except:
        return False, val
    

    
def isFloat(val):
    try:
        return True, float(val)
    except:
        return False, val
    
def stripPunctuationAndWhiteSpace(val):
    return val.translate(None, string.punctuation).strip()
    
def loadSuburbs():
    df = pd.read_csv(DATA_FILE_POSTCODES)
    df = df.drop(['postcode'], axis=1)
    df['suburb'] = map(lambda x: x.upper(), df['suburb'])
    df['state'] = map(lambda x: x.upper(), df['state'])
    df.drop_duplicates(inplace=True)
    # Sort by descending order of length of names so that search is better
    df['namelen'] = map(lambda x: len(x), df['suburb'])
    df.sort_values('namelen', ascending=False, inplace=True)
    df.drop(['namelen'],axis=1, inplace=True)
    return df

def matchSuburbFromDataFrame(df, line):
    merchant=line.upper()
    suburb = None
    lat = None
    lng = None 
    names = df['suburb'].values.tolist()
    for index, row in df.iterrows():
        suburbName = row['suburb']
        suburbLoc = merchant.rfind(suburbName)
        if suburbLoc < 0:
            matches = difflib.get_close_matches(suburbName, merchant.split(), cutoff=0.8)
            if matches:
                match = matches[0]
                suburbLoc = merchant.rfind(match)
        if suburbLoc >= 0:
            merchant = line[0:suburbLoc]
            suburb=suburbName
            lat=row['latitude']
            lng=row['longitude']
            break
     
    return merchant, suburb, lat, lng


cbaline1="LITTLE INDIA - HARRIS HARRIS PARK NS AUS Card xx7113 Value Date: 09/09/2017"
cbaline2="Wdl ATM CBA ATM  SUTHERLAND     NSW 225901   AUS"
def parseCBADescription(suburbsDf, line):
    merchant, suburb, lat, lng = matchSuburbFromDataFrame(suburbsDf, line)
    def removeKnownStrings(desc):
        cardLoc = desc.rfind("CARD XX")
        if cardLoc >= 0:
            desc = desc[0:cardLoc]
        return desc
        
    merchant = stripPunctuationAndWhiteSpace(removeKnownStrings(merchant))
    if merchant == None:
        merchant = 'UNKNOWN'
    if suburb == None:
        suburb = 'UNKNOWN'
    return merchant,suburb,lat,lng
            
bendigoline1="RETAIL PURCHASE TASTE BAGUETTE 2,NEY NSW 1407 AUD000000001000"
bendigoline2="INTERNATIONAL TRANSACTION FEE"
bendigoline3="RETAIL PURCHASE TPG INTERNET PTY LT,NORTH RYDE 3103 AUD000000005999"
def parseBendigoDescription(suburbsDf, line):
    merchant, suburb, lat, lng = matchSuburbFromDataFrame(suburbsDf, line)
    def removeKnownStrings(desc):
        loc = desc.find("RETAIL PURCHASE")
        if loc >= 0:
            desc = desc[loc + len("RETAIL PURCHASE"):]
        return desc
    merchant = stripPunctuationAndWhiteSpace(removeKnownStrings(merchant))
    if merchant == None:
        merchant = 'UNKNOWN'
    if suburb == None:
        suburb = 'UNKNOWN'
    return merchant,suburb,lat,lng
            
anzline1="STEPHEN CHUNGHAN YOON SYDNEY OLYMPI"
anzline2="GITHUB.COM CLN2E 4154486673 7.00 USD 0.27 AUD"
anzline3="Pablo & Rusty's 161 North Ryde"
def parseANZDescription(suburbsDf, line):
    merchant, suburb, lat, lng = matchSuburbFromDataFrame(suburbsDf, line)
    merchant = stripPunctuationAndWhiteSpace(merchant)
    if merchant == None:
        merchant = 'UNKNOWN'
    if suburb == None:
        suburb = 'UNKNOWN'
    return merchant,suburb,lat,lng
            
    