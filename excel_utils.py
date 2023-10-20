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

    
    #draw frame borders
    thick = 2

    draw_frame_border(workbook,worksheet,0,0,2,3,thick)
    draw_frame_border(workbook,worksheet,0,3,2,2,thick)
    draw_frame_border(workbook,worksheet,0,5,2,2,thick)
    draw_frame_border(workbook,worksheet,0,7,2,2,thick)
    draw_frame_border(workbook,worksheet,0,9,2,2,thick)
    draw_frame_border(workbook,worksheet,0,11,2,2,thick)
    draw_frame_border(workbook,worksheet,0,13,2,2,thick)
    draw_frame_border(workbook,worksheet,0,15,2,2,thick)

    #draw frame border function works a bit wonky...reference is from bottow row of prev commands
    #added "-2" to max_row in order to account for offset from previous border draws
    draw_frame_border(workbook,worksheet,2,0,max_row-2,3,thick)
    draw_frame_border(workbook,worksheet,2,3,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,5,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,7,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,9,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,11,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,13,max_row-2,2,thick)
    draw_frame_border(workbook,worksheet,2,15,max_row-2,2,thick)
    


    #generate formats
    row0_format = workbook.add_format({'text_wrap' : True, 'bold':True}) # type: ignore
    #row1_format = workbook.add_format({'bold': True, 'bottom': 5}) #type: ignore
    row1_format = workbook.add_format({'bold': True}) #type: ignore

    # format the top row
    worksheet.set_row(0,45,row0_format)       #Top Row Height allows 3 lines
    worksheet.set_row(1,None,row1_format)


    worksheet.set_column(0, 0, 28)  #District Name
    worksheet.set_column(1,1,10)     #District ID
    worksheet.set_column(2,2,10)     #Year
    worksheet.set_column(3,max_col-1,15) # The rest of the columns

    #freeze the top two rows
    worksheet.freeze_panes(2,0)
    
    #turn on autofilters
    worksheet.autofilter(1,0,max_row,max_col -1)
    
    writer.close()

# Format cell borders via a configurable RxC box
def draw_frame_border(workbook, worksheet, first_row, first_col, rows_count, cols_count,thickness=1):

    if cols_count == 1 and rows_count == 1:
        # whole cell
        worksheet.conditional_format(first_row, first_col,
                                     first_row, first_col,
                                     {'type': 'formula', 'criteria': 'True',
                                     'format': workbook.add_format({'top': thickness, 'bottom':thickness,
                                                                    'left': thickness,'right':thickness})})    
    elif rows_count == 1:
        # left cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness,'bottom':thickness})})
        # top and bottom sides
        worksheet.conditional_format(first_row, first_col + 1,
                                 first_row, first_col + cols_count - 2,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': thickness,'bottom':thickness})})

        # right cap
        worksheet.conditional_format(first_row, first_col+ cols_count - 1,
                                 first_row, first_col+ cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'right': thickness,'bottom':thickness})})

    elif cols_count == 1:
        # top cap
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness,'right':thickness})})

        # left and right sides
        worksheet.conditional_format(first_row + 1,              first_col,
                                 first_row + rows_count - 2, first_col,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': thickness,'right':thickness})})

        # bottom cap
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'left': thickness,'right':thickness})})

    else:
        # top left corner
        worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'left': thickness})})

        # top right corner
        worksheet.conditional_format(first_row, first_col + cols_count - 1,
                                 first_row, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'top': thickness, 'right': thickness})})

        # bottom left corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'left': thickness})})

        # bottom right corner
        worksheet.conditional_format(first_row + rows_count - 1, first_col + cols_count - 1,
                                 first_row + rows_count - 1, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': thickness, 'right': thickness})})

        # top
        worksheet.conditional_format(first_row, first_col + 1,
                                     first_row, first_col + cols_count - 2,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'top': thickness})})

        # left
        worksheet.conditional_format(first_row + 1,              first_col,
                                     first_row + rows_count - 2, first_col,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': thickness})})

        # bottom
        worksheet.conditional_format(first_row + rows_count - 1, first_col + 1,
                                     first_row + rows_count - 1, first_col + cols_count - 2,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'bottom': thickness})})

        # right
        worksheet.conditional_format(first_row + 1,              first_col + cols_count - 1,
                                     first_row + rows_count - 2, first_col + cols_count - 1,
                                     {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'right': thickness})})