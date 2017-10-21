import parseutils as pu
import modelutils as mu
import pandas as pd
import numpy as np
from functools import partial

def _loadDetectors():
    success, clf, vec, lbl = mu.loadBankDetectorModels()
    if not success:
        raise clf
    return clf, vec, lbl

def _detect(descriptionDf):
    if descriptionDf.empty:
        return None
    clf,vec,lbl = _loadDetectors()
    # use 10% of data to detect the bank
    # for prediction with max frequency wins
    sample = descriptionDf.sample(frac=0.1)
    # get vectorized inputs
    x = vec.transform(descriptionDf.values).todense()
    # convert them to classes under column 'bank'
    df = pd.DataFrame({'bank':lbl.classes_[clf.predict(x)]})
    # count their frequencies and sort in descending order
    df = pd.value_counts(df['bank'].values, sort=True)
    # print df
    # return the index of the top on (the bank label from classifier)
    return df.index[0], clf, vec, lbl

def _loadCsvAndGetColumnIndices(pathToCsv):
    csvDf = pd.read_csv(pathToCsv, header=None).head(100)
    midPoint = csvDf.loc[len(csvDf)//2]
    #use this row to try to deduce date, amount and description column indices
    dateIdx=None
    amountIdx=None
    descIdx=None
    for c in csvDf.columns:
        val = midPoint[c]
        if (dateIdx is not None) and (amountIdx is not None) and (descIdx is not None):
            break
        isDate,dt = pu.isDate(val)
        isAmt,_ = pu.isFloat(val)
        if isAmt and (amountIdx is None):
            amountIdx = c
            continue
        
        # This needs to be after amount parsing due to lenient parsing of date
        if isDate and (dateIdx is None):
            dateIdx=c
            continue

        if descIdx is None:
            if (not isAmt) and (not isDate):
                descIdx = c
                continue
    
    if (dateIdx is None) or (amountIdx is None) or (descIdx is None):
        raise "Not all columns could be found in csv. Check data format"
    #return data
    return {'Date':dateIdx, 'Amount':amountIdx, 'Description':descIdx}, csvDf


def loadAndNormalize(pathToCsv):
    colIndices,df = _loadCsvAndGetColumnIndices(pathToCsv)
    bank, clf, vec, lbl = _detect(df[colIndices['Description']])
    suburbsDf = pu.loadSuburbs()
    
    COL_NAME_DATE='Date'
    COL_NAME_DAY='Day'
    COL_NAME_MONTH='Month'
    COL_NAME_YEAR='Year'
    COL_NAME_WEEKDAY='Weekday'
    COL_NAME_AMOUNT='Amount'
    COL_NAME_DESC='Description'
    COL_NAME_BANK='Bank'
    COL_NAME_MERCHANT='Merchant'
    COL_NAME_SUBURB='Suburb'
    COL_NAME_LAT='Latitude'
    COL_NAME_LNG='Longitude'
    
    def retainDateAmountAndDescription(df, bank):
        dateIdx, amountIdx, descIdx = colIndices['Date'], colIndices['Amount'], colIndices['Description'] 
        # move columns to 'Date', 'Amount', 'Description' order, discard other columns
        newCols=[dateIdx,amountIdx,descIdx]
        df = df.ix[:,newCols]
        dateIdx, amountIdx, descIdx = 0,1,2 #after moving columns
        df[dateIdx] = map(lambda x: pu.isDate(x)[1], df[dateIdx])
        df[amountIdx] = map(lambda x: pu.isFloat(x)[1], df[amountIdx])
        #give names to the first 3 columns
        df.columns = [COL_NAME_DATE, COL_NAME_AMOUNT, COL_NAME_DESC]
        df.insert(1,COL_NAME_WEEKDAY, map(lambda d: d.weekday(), df[COL_NAME_DATE]))
        df.insert(1,COL_NAME_YEAR, map(lambda d: d.year, df[COL_NAME_DATE]))
        df.insert(1,COL_NAME_MONTH, map(lambda d: d.month, df[COL_NAME_DATE]))
        df.insert(1,COL_NAME_DAY, map(lambda d: d.day, df[COL_NAME_DATE]))
        df.insert(len(df.columns),COL_NAME_BANK, bank)
        return df
    
    def getParseFunction(bank):        
        if bank == 'CBA':
            return pu.parseCBADescription
        elif bank == 'BENDIGO':
            return pu.parseBendigoDescription
        else:
            return pu.parseANZDescription
        
    def addColumnsFromParseFuncOutput(df, parseFunc):
        def addLastColumn(df, colName, colVal):
            df.insert(len(df.columns), colName, colVal)
        #Create new columns
        addLastColumn(df, COL_NAME_MERCHANT, 'UNKNOWN')
        addLastColumn(df, COL_NAME_SUBURB, 'UNKNOWN')
        addLastColumn(df, COL_NAME_LAT, None)
        addLastColumn(df, COL_NAME_LNG, None)
        #add values into these columns
        for idx,row in df.iterrows():
            line = row['Description']
            merchant, suburb, lat, lng = parseFunc(line)
            #print "M: ", merchant, "S: ", suburb
            df.at[idx, COL_NAME_MERCHANT] = merchant
            df.at[idx, COL_NAME_SUBURB] = suburb
            df.at[idx, COL_NAME_LAT] = lat
            df.at[idx, COL_NAME_LNG] = lng
        return df

        
    
    df = retainDateAmountAndDescription(df, bank)
    parseFunc = partial(getParseFunction(bank), suburbsDf)
    df = addColumnsFromParseFuncOutput(df,parseFunc)
    return df
                      
    
    
    
