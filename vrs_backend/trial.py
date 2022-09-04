import pdfplumber
import pandas as pd

pdf = pdfplumber.open(
    "/home/drivetech-sayali/Downloads/VSReports/VehicleReport__Z101-D-MT-2WD_PRO-LUXURY_22-08-2022-19-12-12-7600246_MA1TJ2YD6N6G95596_62 Km.pdf")

tables = []
tablesDict = {}
tempEcuName = ""

for page in pdf.pages:
    tables.extend(page.extract_table())

tablesDf = pd.DataFrame(tables[1:], columns=tables[0])
tablesDf.drop(['Active'], axis=1)

for index in range(len(tablesDf)):
    if tablesDf['EcuName'][index] != "":
        tempEcuName = tablesDf['EcuName'][index]
        tablesDict[tablesDf['EcuName'][index]] = [(
            tablesDf['Parameter'][index], tablesDf['Value'][index])]
    else:
        tablesDict[tempEcuName].append((
            tablesDf['Parameter'][index], tablesDf['Value'][index]))

print(tablesDict)