def seqToCode(seq):
    code = ''
    usedCodeValues = {}
    codeValue = 'a'
    for el in seq:
        if el in usedCodeValues:
            code += usedCodeValues[el]
        else:
            code += codeValue
            usedCodeValues[el] = codeValue
            codeValue = chr(ord(codeValue) + 1)
    return code

def provide_culture_and_culture_group_encodings(df):
    df['cultuCode'] = df.apply(lambda row: seqToCode([row[column] for column in df.columns if column.startswith('CODE_CULTU_')]), axis=1)
    df['groupCode'] = df.apply(lambda row: seqToCode([row[column] for column in df.columns if column.startswith('CODE_GROUP_')]), axis=1)