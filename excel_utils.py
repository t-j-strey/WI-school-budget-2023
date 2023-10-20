import pandas as pd



def create_title(report):
    title = report.strip("https://sfs.dpi.wi.gov/sfsdw/")
    title = title.strip(".aspx")
    title = title + ".xlsx"
    return title


def export_workbook(title,df):
    writer = pd.ExcelWriter(title,
                                    engine = 'xlsxwriter',
                                    mode = 'w'
                                    )
    df.to_excel(writer,
                        sheet_name='Sheet1',
                        index = False,
                        header = False,
                        merge_cells = True)
    workbook = writer.book
    
    worksheet = writer.sheets["Sheet1"]
    (max_row,max_col) = df.shape

    #generate formats
    row0_format = workbook.add_format({'text_wrap' : True, 'bold':True}) # type: ignore
    row1_format = workbook.add_format({'bold': True, 'bottom': 5}) #type: ignore

    # format the top row
    worksheet.set_row(0,45,row0_format)       #Top Row Height allows 3 lines
    worksheet.set_row(1,None,row1_format)


    worksheet.set_column(0, 0, 30)  #District Name
    worksheet.set_column(1,1,6)     #year
    worksheet.set_column(2,max_col-1,15) # The rest of the columns

    #freeze the top two rows
    worksheet.freeze_panes(2,0)
    
    #turn on autofilters
    worksheet.autofilter(1,0,max_row,max_col -1)
    
    writer.close()