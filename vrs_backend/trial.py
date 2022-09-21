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


# from bs4 import BeautifulSoup

# filepath = "/home/drivetech-sayali/Downloads/VSR1/M62021_MCAPJ8AY1PFA01968_892022_165725(after).htm"

# with open(filepath, 'r') as f:
#     contents = f.read()
#     soup = BeautifulSoup(contents, 'lxml')

# variant_code = '62 20 23 35 39 35 39 36 30 35 37 35 39 34 4F 55 54 50 55 54 44 4A 49 54 20 22 04 14 4F 0C 44 85 10 42 05 00 22 00 02 00 00 00 01 00 4F 0C 44 05 10 40 01 00 22 00 02 00 00 00 00 00 59 E8 6D F2 8C 80 08 87 61 33 08 D7 45 20 78 03 A3 1E 50 52 80 35 13 14 00 43 02 30 00 43 90 20 00 03 07 00 A4 82 10 EE 00 00 20 34 94 09 01 70 EB 5E 46 AD 40 64 28 09 C6 10 02 C0 04 29 00 E7 08 91 4C 17 60 00 49 00 0A 9A CB 2B 89 49 00 01 00 00 40 20 00 00 19 11 21 22 04 70 05 00 00 00 00 00 00 00 01 01 03 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00 80 01 00 02 00 00 00 00 00 03 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'

# text_soup = soup.get_text()


# print(text_soup.find(variant_code))

from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io


food_calories = read_pdf('./data/food_calories.pdf',pages = 6, 
                         multiple_tables = True, stream = True)

# Transform the result into a string table format
table = tabulate(food_calories)

# Transform the table into dataframe
df = pd.read_fwf(io.StringIO(table))