# import pdfplumber
# import pandas as pd

# pdf = pdfplumber.open(
#     "/home/drivetech-sayali/Downloads/VSReports/VehicleReport__Z101-D-MT-2WD_PRO-LUXURY_22-08-2022-19-12-12-7600246_MA1TJ2YD6N6A13579_30 Km-1.pdf")

# tables = []
# tablesDict = {}
# tempEcuName = ""

# for page in pdf.pages:
    # print(page.extract_table())
    # tables.extend(page.extract_table())
    # break
# print([subT[:4] for subT in tables[1:]])
# tablesDf = pd.DataFrame(tables[1:], columns=tables[0])
# tablesDf.drop(['Active'], axis=1)
# print(tablesDf)
# for index in range(len(tablesDf)):
#     if tablesDf['EcuName'][index] != "":
#         tempEcuName = tablesDf['EcuName'][index]
#         tablesDict[tablesDf['EcuName'][index]] = [(
#             tablesDf['Parameter'][index], tablesDf['Value'][index])]
#     else:
#         tablesDict[tempEcuName].append((
#             tablesDf['Parameter'][index], tablesDf['Value'][index]))

# print(tablesDict)


from bs4 import BeautifulSoup

filepath = "/home/drivetech-sayali/Downloads/VSR/M62021_MCAPJ8AY9PFA00289_542022_203215.htm"

with open(filepath, 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')

print(soup)