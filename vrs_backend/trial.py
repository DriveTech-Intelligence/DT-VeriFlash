import pdfplumber


pdf = pdfplumber.open("/home/drivetech-sayali/Downloads/VehicleReport__Z101-D-MT-2WD_PRO-LUXURY_22-08-2022-19-12-12-7600246_MA1TJ2YD6N6G95596_62 Km.pdf")
headerName = pdf.pages[0].extract_table()[0]

print(headerName)

for page in pdf.pages:
  print(page.extract_table())