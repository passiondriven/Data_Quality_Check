'''
data quality check for pandas dataframes
'''

def quality_check(table,empty='',show_correct=True):    
    try:
        from IPython.display import Markdown, display
        jupyter_environment=True
        def print_MD(string, color=None):  # result with Markdown formating
            colorstr = "<span style='color:{}'>{}</span>".format(color, string)
            display(Markdown(colorstr))
        def print_and_print_MD(text, l_just=50, color=None):
            print(text.ljust(l_just,'.')) if jupyter_environment==False else print_MD(text.ljust(l_just,'.'), color=color)            
    except:
        jupyter_environment=False
        
    # settings ----------------
    
    max_table_lenght=50  # max row count for tables in results (larger than that and you get only problem count)
    unique_numbers_at_least=0.9  # it is 90%  (dor number outliers)
    less_than_percent=0.01 # it is 1%  (for value count outliers)
    #empty=''  # '' this setting looks for empty and NaN  (for empty values)
    numbers_at_least=0.9; ignore_empty=True; show_problems=True  # check of there are only number in number column
    unique_values_at_least=0.95 # it is 95%  (duplicate test)
    symbol_group_under_percent=0.02; symbol_group_over_percent=0.15 # it is 2% and 15%  (string lengts by rows)
    string_group_under_percent=0.02; string_group_over_percent=0.15;symbol_count=2 # tas ir 2% un 15%  (string begining group check)
    
    # ---------------------------------
    
    def column_title():  # column title
        title = '  Column name: " ' + col + ' "  '
        print('\n')
        print(title.ljust(150,'-') + '\n') if jupyter_environment==False \
        else print_MD('**' + title.center(100,'-') + '** \n')
        
    
    for col in table.columns:
        tilte_already_is=False
        
        # if column have more than 1 data type
        if len(table[col].map(type).value_counts())!=1 and len(table[table[col].notna()][col].map(type).value_counts())!=0:
            column_title()
            tilte_already_is=True
            print_and_print_MD('More than one data type ', color='red')
            type_table = pd.DataFrame(table[table[col].notna()][col].map(type).value_counts())
            type_table.reset_index(level=0, inplace=True)
            type_table.columns = ['data type', 'row count']
            print(type_table) if jupyter_environment==False else display(type_table)                
        
        # number outlier
        at_least_1_problem = False
        if pd.to_numeric(table[col], errors='coerce').notnull().all() and len(table[col]) * \
        unique_numbers_at_least>=len(table[col].unique()):
            try:
                Q1 = table[col].quantile(0.25)
                Q3 = table[col].quantile(0.75)
                IQR = Q3 - Q1
                result_under = table[table[col]< Q1 - 1.5 * IQR][col].unique()
                result_over = table[table[col]> Q3 + 1.5 * IQR][col].unique()
                if len(result_under)>0 or len(result_over)>0:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('Anomalys in number values ', color='red')                
                if len(result_under)>0:
                    if len(result_under)<=max_table_lenght:
                        print_and_print_MD('- Strangly small values ' + str(list(set(result_under))), 0, color=None)
                    else:
                        print_and_print_MD('- Too many problems found while using current settings: ' + str(len(result_under)) + ' rows. Results will not be displayed in table', 0, color=None)
                    at_least_1_problem = True
                if len(result_over)>0:
                    if len(result_over)<=max_table_lenght:
                        print_and_print_MD('- Strangly large values ' + str(list(set(result_over))), 0, color=None)
                    else:
                        print_and_print_MD('- Too many problems found while using current settings: ' + str(len(result_over)) + ' rows. Results will not be displayed in table', 0, color=None)
                    at_least_1_problem = True
                if at_least_1_problem==False and show_correct==True:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('Anomalys in number values ', color='green')
                    print_and_print_MD('- Anomalys not found ', 0, color=None)
            except:
                if show_correct==True:
                    print_and_print_MD('Anomalys in number values ', color=None) 
                    print_and_print_MD('- Checking this is not needed', 0, color=None)
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('Anomalys in number values ', color=None) 
                print_and_print_MD('- Checking this is not needed', 0, color=None)
        
        # value count outlier
        at_least_1_problem = False
        new_table = pd.DataFrame(table[col].value_counts())
        new_table.reset_index(level=0, inplace=True)
        new_table.columns = [col, 'count']
        new_table['percent from column'] = new_table['count'] / sum(new_table['count'])
        new_table_filtreta = new_table[new_table['percent from column']<less_than_percent]
        if len(new_table)<len(table[col].unique())*0.1: # if result has less than 10% unique, then those are problems
            if len(new_table_filtreta)>0:
                at_least_1_problem = True
                if jupyter_environment==False:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print('\nAnomalys in value counts '.ljust(50,'.'))
                    print(new_table_filtreta) if len(new_table_filtreta)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_table_filtreta)) + ' rows. Results will not be displayed in table')
                else:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_MD('\nAnomalys in value counts '.ljust(50,'.'), color='red')
                    display(new_table_filtreta.style.hide_index()) if len(new_table_filtreta)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_table_filtreta)) + ' rows. Results will not be displayed in table')
            else:
                if at_least_1_problem==False and show_correct==True:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('\nAnomalys in value counts ', color='green')
                    print_and_print_MD('- Anomalys not found ', 0, color=None)
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nAnomalys in value counts ', color=None)
                print_and_print_MD('- Checking this is not needed', 0, color=None)
            
        # missing values
        was_empty = False      
        empty_count = table[col].isna().sum() if table[col].isna().sum()>0 and empty=='' else len(table[table[col]==empty])        
        if empty_count>0:
            if tilte_already_is==False:
                column_title()
                tilte_already_is=True
            print_and_print_MD('\nMissing values ', color='red')
            empty_proc = str(round(empty_count/len(table[col])*100,2))
            print_and_print_MD('- Found: ' + str(empty_count) + ' empty cells. Empty are ' + empty_proc + '% of all cells in this column', 0, color=None)
            was_empty = True
        if was_empty == False and show_correct==True:
            if tilte_already_is==False:
                column_title()
                tilte_already_is=True
            print_and_print_MD('\nMissing values ', color='green')
            print_and_print_MD('- If empty set as " ' + empty + '", then there are no empty cells', color=None)        
        
        # nonnumeric symbols in number columns
        at_least_1_problem = False
        empty_count = table[col].isna().sum() if table[col].isna().sum()>0 and empty=='' else len(table[table[col]==empty])
        rindu_kopskaits = len(table) - empty_count if ignore_empty==True else len(table)
        if len(table.loc[table[col].astype(str).str.isnumeric()]) / rindu_kopskaits > numbers_at_least:
            test = pd.to_numeric(table[col], errors='coerce').notnull().all()  # parāda True vai False
            if test == False:
                at_least_1_problem = True
                if show_problems==True:
                    kludas = pd.DataFrame({'Problems:':table[col].unique()})
                    kludu_saraksts = kludas[~kludas['Problems:'].astype(str).str.isnumeric()]['Problems:'].tolist()
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('\nNonnumeric symbols in number columns ', color='red')
                    print_and_print_MD('- Problems found: ' + str(len(kludu_saraksts)), 0, color=None)
                    print(kludu_saraksts) if len(kludu_saraksts)<=max_table_lenght else print_and_print_MD('- Too many problems found while using current settings: ', 0, color=None)
            if at_least_1_problem == False and show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nNonnumeric symbols in number columns ', color='green')
                print_and_print_MD('- There are only number in this column', 0, color=None)
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nNonnumeric symbols in number columns ', color=None)
                print_and_print_MD('- Checking this is not needed', 0, color=None)
            
        # duplicates test
        at_least_1_problem = False
        if len(table[col].unique())/len(table[col]) > unique_values_at_least and len(table[table[col].duplicated(keep=False)])/len(table[col])!=0 and len(table[table[col].duplicated(keep=False)])/len(table[col])!=1:
            if len(table[table[col].duplicated(keep=False)])!=0:
                at_least_1_problem = True
                if jupyter_environment==False:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print('\nChecking duplicated values '.ljust(50,'.'))
                    print(table[table[col].duplicated(keep=False)].sort_values(by=col)) if len(table[table[col].duplicated(keep=False)])<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(table[table[col].duplicated(keep=False)])) + ' rows. Results will not be displayed in table')
                else:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_MD('\nChecking duplicated values '.ljust(50,'.'), color='red')
                    display(table[table[col].duplicated(keep=False)].sort_values(by=col).style.hide_index().set_properties(**{'background-color': '#FDFDD2'}, subset=col)) if len(table[table[col].duplicated(keep=False)])<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(table[table[col].duplicated(keep=False)])) + ' rows. Results will not be displayed in table')
            if at_least_1_problem == False and show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nChecking duplicated values ', color='green')
                print_and_print_MD('- There are no problems with duplicated values', 0, color=None)
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nChecking duplicated values ', color=None)
                print_and_print_MD('- Checking this is not needed', 0, color=None)
        
        # string lenght differences by rows
        new_df = pd.DataFrame(table[table[col].notna()])
        new_df['symbol_count'] = table[col].astype(str).str.len()
        new_df = pd.DataFrame(new_df['symbol_count'].value_counts())
        new_df.reset_index(level=0, inplace=True)
        new_df.columns = ['symbol_count', 'row_count']
        new_df['part_size_(%)'] = round(new_df['row_count'] / sum(new_df['row_count'])*100,2)
        if len(new_df[new_df['part_size_(%)']>symbol_group_over_percent])>0:
            if len(new_df[new_df['part_size_(%)']<symbol_group_under_percent])>0:
                if jupyter_environment==False:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print('\nString lenght differences by rows '.ljust(50,'.'))
                    print(new_df) if len(new_df)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_df)) + ' rows. Results will not be displayed in table')
                else:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_MD('\nString lenght differences by rows '.ljust(50,'.'), color='red')
                    def row_color(table):
                        if table['part_size_(%)'] < symbol_group_under_percent*100:
                            return ['background-color: #FDFDD2'] * len(table)
                        else:
                            return ['background-color: #DBFECD'] * len(table)
                    f = {'part_size_(%)':'{:.2f}'}
                    display(new_df.style.format(f).apply(row_color, axis=1).hide_index()) if len(new_df)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_df)) + ' rows. Results will not be displayed in table')
            else:
                if show_correct==True:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('\nString lenght differences by rows ', color=None)
                    print_and_print_MD('- Problems not found', 0, color='green')
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nString lenght differences by rows ', color=None)
                print_and_print_MD('- Checking this is not needed', 0, color=None)
                
        # string begining differences by rows
        new_df = pd.DataFrame(table[table[col].notna()])     
        new_df['string_begining'] = new_df[col].astype(str).str[:symbol_count]
        new_df = pd.DataFrame(new_df['string_begining'].value_counts())
        new_df.reset_index(level=0, inplace=True)
        new_df.columns = ['string_begining', 'row_count']
        new_df['part_size_(%)'] = round(new_df['row_count'] / sum(new_df['row_count'])*100,2)
        if len(new_df[new_df['part_size_(%)']>string_group_over_percent])>0:
            if len(new_df[new_df['part_size_(%)']<string_group_under_percent])>0:
                if jupyter_environment==False:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print('\nString begining differences by rows '.ljust(50,'.'))
                    print(new_df) if len(new_df)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_df)) + ' rows. Results will not be displayed in table')
                else:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_MD('\nString begining differences by rows '.ljust(50,'.'), color='red')
                    def row_color(table):
                        if table['part_size_(%)'] < string_group_under_percent*100:
                            return ['background-color: #FDFDD2'] * len(table)
                        else:
                            return ['background-color: #DBFECD'] * len(table)
                    f = {'part_size_(%)':'{:.2f}'}
                    display(new_df.style.format(f).apply(row_color, axis=1).hide_index()) if len(new_df)<=max_table_lenght else print('- Too many problems found while using current settings: ' + str(len(new_df)) + ' rows. Results will not be displayed in table')
            else:
                if show_correct==True:
                    if tilte_already_is==False:
                        column_title()
                        tilte_already_is=True
                    print_and_print_MD('\nString begining differences by rows ', color=None)
                    print_and_print_MD('- Problems not found', 0, color='green')
        else:
            if show_correct==True:
                if tilte_already_is==False:
                    column_title()
                    tilte_already_is=True
                print_and_print_MD('\nString begining differences by rows ', color=None)
                print_and_print_MD('- Checking this is not needed', 0, color=None)
