'''
This file looks into the Vehicle Scan report(VSR) and captures vin, date, part number to 
generate a summary report for all the files together into a excel sheet.

'''

import pandas as pd
import os
from dataclasses import dataclass
import datetime

#Data class for storing information per file per flash
@dataclass
class Flash_info:
    vin : str
    date : datetime.datetime
    part_number : str
    file_name : str
    pwt_code : str


class VSR:
    def __init__(self, pre='AF', post='AG'):
        self.pre_flash = {}
        self.post_flash = {}
        self.preFlash = pre
        self.postFlash = post
        self.flash_df = pd.DataFrame(columns=['VIN','Pre_flash','Post_flash','PWT','Status','Date','Filename'])
        self.vin_set = set()
        self.pwt = {'216':'9AT FWD', '217':'9AT 4*4', '218':'6MT FWD'}


    def get_date(self, df, pattern):
        df = df[df.apply(lambda x: x.str.contains(pattern, regex=True))].dropna(how='all').reset_index(drop=True)
        df = df.dropna(axis=1, how='all').iat[0,0]
        return df


    def get_info(self, folder_path, file_name):
        fn = os.path.join(folder_path,file_name)

        df = pd.read_html(fn)
        date = df[0]
        ecu_df = df[1]

        try:
            vin = file_name.split("_")[1]
        except IndexError:
            vin = file_name.split(".")[0]
        date = self.get_date(date,'^Date:.*')[5:]
        date = datetime.datetime.strptime(date, "%A, %B %d %Y %I:%M:%S %p")
        part_number = ecu_df.loc[ecu_df['ECU']=='PCM']['Part Number'].reset_index(drop=True)[0]

        pwt_code = part_number[-5:-2]
    
        return Flash_info(vin, date, part_number, file_name, pwt_code)


    def create_summary_report(self, folder_path):
        for f in os.listdir(folder_path):
            if f.endswith('.htm') or f.endswith('.html'):
                
                info = self.get_info(folder_path,f)
                # print("Filename "+f+"\tpartnumber " +info.part_number+"\t VIN "+info.vin)

                self.vin_set.add(info.vin)
                # print(len(self.vin_set))

                if info.part_number.endswith(self.preFlash):
                    self.pre_flash[info.vin] = info
                elif info.part_number.endswith(self.postFlash):
                    self.post_flash[info.vin] = info
        self.process_flashInfo()
        self.create_excel(folder_path)

        print("Please checkout the report in folder: "+folder_path)
        return self.flash_df


    def process_flashInfo(self):
        for vin in self.vin_set:
            pre = None
            post = None

            if vin in self.pre_flash.keys():
                pre = self.pre_flash[vin]
            if vin in self.post_flash.keys():
                post = self.post_flash[vin]

        
            if pre is not None and post is not None:
                if pre.part_number[:-2] == post.part_number[:-2]:
                    l = [vin, pre.part_number, post.part_number, self.pwt[post.pwt_code], 'OK', post.date, post.file_name]
                    self.flash_df.loc[len(self.flash_df)] = l
                else:
                    l = [vin, pre.part_number, post.part_number,self.pwt[post.pwt_code], 'Failed', post.date, post.file_name]
                    self.flash_df.loc[len(self.flash_df)] = l
            elif pre is None and post is not None:
                l = [vin, " ", post.part_number,self.pwt[post.pwt_code], 'OK', post.date, post.file_name]
                self.flash_df.loc[len(self.flash_df)] = l
            elif pre is not None and post is None:
                l = [vin, pre.part_number, " ",self.pwt[pre.pwt_code], 'TBD', " ", " "]
                self.flash_df.loc[len(self.flash_df)] = l
    

    def create_excel(self, path):
        writer = pd.ExcelWriter(os.path.join(path,'VSR_'+str(datetime.datetime.now())+'.xlsx'), engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        self.flash_df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']


        # Add a format. Light red fill with dark red text.
        format_error = workbook.add_format({'font_color': '#9C0006'})
        format_ok = workbook.add_format({'font_color': '#00FF00'})
        format_tbd = workbook.add_format({'font_color': '#FFA500'})

        # text_format = workbook.add_format({'text_wrap': True})
        # cell_format = workbook.add_format()
        # cell_format.set_text_wrap()
        
        # Set the conditional format range.
        start_row = 0
        start_col = 4
        end_row = len(self.flash_df)
        end_cold = start_col

        # Apply a conditional format to the cell range.
        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                    {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"Failed"',
                                    'format':   format_error})
        
        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                    {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"OK"',
                                    'format':   format_ok})

        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                    {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"TBD"',
                                    'format':   format_tbd})

        # worksheet.set_row(start_row, end_row, cell_format)
        # worksheet.set_column(start_col, end_cold, cell_format)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        
# if __name__ == '__main__':
#     vsr = VSR(pre='AG', post='AI')
#     df = vsr.create_summary_report("/home/drivetech-sayali/Downloads/08-08-2022-20220817T012151Z-001/08-08-2022/NOIDA")
#     print(df)