import os
import csv
from utils.parsers.JSONparsers import basicParser
from openpyxl import Workbook
from openpyxl.styles import Font



def write_markdown_report(table, recognizers, filename):
    # Build header rows
    header = ["SAMPLE"]
    for recog in recognizers:
        name = recog.__name__
        header.append(f"{name} SCORE")
        header.append(f"{name} PASS")


    #  Build separator row (alignment row)
    #    Left for SAMPLE and PASS
    #    Right for SCORE

    separator = [":--"]  # SAMPLE left aligned
    for _ in recognizers:
        separator.append("--:")   # SCORE right
        separator.append(":--")   # PASS left

    #  Write file
    with open(filename, "w") as f:
        # First header row
        f.write("| " + " | ".join(header) + " |\n")
        # Alignment separator
        f.write("| " + " | ".join(separator) + " |\n")
 
        # Data rows
        for row in table:
            md_row = [row[0]]
            for (p, s) in row[1:]:
                status = "🟢 PASS" if p else "🔴 FAIL"
                md_row.append(f"{s:.1f}")
                md_row.append(status)
            f.write("| " + " | ".join(md_row) + " |\n")



def write_xlsx_report(table, recognizers, filename):

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # Headers (two rows)
    header_row1 = ["SAMPLE"]
    header_row2 = [""]
    for recog in recognizers:
        header_row1.append(recog.__name__)
        header_row1.append("")
        header_row2.append("PASS")
        header_row2.append("SCORE")
    ws.append(header_row1)
    ws.append(header_row2)

    # Merge recognizer header cells
    col = 2
    for _ in recognizers:
        ws.merge_cells(start_row=1, start_column=col,
                       end_row=1, end_column=col+1)
        col += 2

    #  Data
    green_font = Font(color="008000")  # green
    red_font = Font(color="FF0000")    # red

    for row in table:
        excel_row = [row[0]]
        for (p, s) in row[1:]:
            excel_row.append("PASS" if p else "FAIL")
            excel_row.append(s)
        ws.append(excel_row)

        # Color PASS/FAIL 
        last_row = ws.max_row
        col_index = 2

        for (p, _) in row[1:]:
            cell = ws.cell(row=last_row, column=col_index)
            if p:
                cell.font = green_font
            else:
                cell.font = red_font
            col_index += 2
    wb.save(filename)



def runRecognizersTest(recognizers, fallSamples, noFallSamples,
                       md_output="testResults/recognizersResults.md",
                       xlsx_output="testResults/recognizersResults.xlsx"):

    # Build unified sample list with ground truth
    samples = []
    for sample in fallSamples:
        samples.append((sample, True))   # True = Fall expected
    for sample in noFallSamples:
        samples.append((sample, False))  # False = NoFall expected


    # Collect structured results
    # [sample_name, (pass_bool, score), (pass_bool, score), ...]
    table = []
    for sample, expected in samples:
        joints = basicParser(sample)
        row = [sample]
        for recog in recognizers:
            detected, score = recog(joints)
            test_pass = detected == expected
            row.append((test_pass, score))
        table.append(row)


    # Write TXT aligned table
    write_markdown_report(table, recognizers, md_output)
    # Write CSV (Excel friendly)
    # write_xlsx_report(table, recognizers, xlsx_output)

    print(f"Reports written to: {md_output} and {xlsx_output}")