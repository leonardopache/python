from openpyxl import Workbook

import readFile

class GenerateReport:
    @staticmethod
    def write_report_xls(root):
        #path_file = (root + '/mutations.csv')
        report_name = '/reportUnit.xlsx'

        #count = readFile()

        lines_covered,lines_total,branch_covered,branch_total = readFile.read_htlm(root)

        report_unit = Workbook()
        worksheet = report_unit.active


        format_percent = report_mutants.add_format()
        format_percent.set_num_format('0.00%')

        format_headline = report_mutants.add_format()
        format_headline.set_bold(True)
        format_headline.set_bg_color('#E6E3E3')

        format_all_mutants = report_mutants.add_format()
        format_all_mutants.set_font_color('blue')

        format_all_mutants_percent = report_mutants.add_format()
        format_all_mutants_percent.set_font_color('blue')
        format_all_mutants_percent.set_num_format('0.00%')


        worksheet.write('A3', 'Mutants by type', format_headline)
        worksheet.write('B3', 'Total Mutants', format_headline)
        worksheet.write('C3', 'Total Mutants Killed', format_headline)
        worksheet.write('D3', '% Mutants per total mutants', format_headline)
        worksheet.write('E3', '% Mutants Killed', format_headline)
        worksheet.write('F3', '% Mutants survived or not covered', format_headline)

        worksheet.write('A4', 'ALL MUTANTS',format_all_mutants)
        worksheet.write('B4', totalMutants,format_all_mutants)
        worksheet.write('C4', totalMutantsKilled,format_all_mutants)
        worksheet.write_formula('E4', '=C4/B4', format_all_mutants_percent)
        worksheet.write_formula('F4', '=1-E4', format_all_mutants_percent)

        worksheet.write('A5', 'ReturnValsMutator')
        worksheet.write('B5', mutantReturnValsMutator)
        worksheet.write('C5', mutantReturnValsMutatorKilled)
        worksheet.write_formula('D5', '=B5/B4', format_percent)
        worksheet.write_formula('E5', '=C5/B4', format_percent)
        worksheet.write_formula('F5', '=D5-E5', format_percent)

        worksheet.write('A6', 'NegateConditionalsMutator')
        worksheet.write('B6', mutantNegateConditionalsMutator)
        worksheet.write('C6', mutantNegateConditionalsMutatorKilled)
        worksheet.write_formula('D6', '=B6/B4', format_percent)
        worksheet.write_formula('E6', '=C6/B4', format_percent)
        worksheet.write_formula('F6', '=D6-E6', format_percent)

        worksheet.write('A7', 'VoidMethodCallMutator')
        worksheet.write('B7', mutantVoidMethodCallMutator)
        worksheet.write('C7', mutantVoidMethodCallMutatorKilled)
        worksheet.write_formula('D7', '=B7/B4', format_percent)
        worksheet.write_formula('E7', '=C7/B4', format_percent)
        worksheet.write_formula('F7', '=D7-E7', format_percent)

        worksheet.write('A8', 'ConditionalsBoundaryMutator')
        worksheet.write('B8', mutantConditionalsBoundaryMutator)
        worksheet.write('C8', mutantConditionalsBoundaryMutatorKilled)
        worksheet.write_formula('D8', '=B8/B4', format_percent)
        worksheet.write_formula('E8', '=C8/B4', format_percent)
        worksheet.write_formula('F8', '=D8-E8', format_percent)

        worksheet.write('A9', 'IncrementsMutator')
        worksheet.write('B9', mutantIncrementsMutator)
        worksheet.write('C9', mutantIncrementsMutatorKilled)
        worksheet.write_formula('D9', '=B9/B4', format_percent)
        worksheet.write_formula('E9', '=C9/B4', format_percent)
        worksheet.write_formula('F9', '=D9-E9', format_percent)

        worksheet.write('A10', 'MathMutator')
        worksheet.write('B10', mutantMathMutator)
        worksheet.write('C10', mutantMathMutatorKilled)
        worksheet.write_formula('D10', '=B10/B4', format_percent)
        worksheet.write_formula('E10', '=C10/B4', format_percent)
        worksheet.write_formula('F10', '=D10-E10', format_percent)

        report_mutants.close()
