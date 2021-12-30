# Data_Quality_Check
Script that automaticaly checks table data for posible errors or anomalys

this function checks for:
•	if column have more than 1 data type
•	number outlier
•	value count outlier
•	missing values
•	nonnumeric symbols in number columns
•	duplicated values
•	string lenght differences by rows
•	string begining symbol differences by rows

quality_check(table,empty='',show_correct=True)
• table - name of your pandas dataframe. for example - df
• empty - what kind of empty values to look for. by defoult empty values are '' (like realy empty space) and it also checks for NaN. You can put any value here.
  Some examples '-' , 'null', '0', '_'
• show_correct - if set to False, shows only problematic results, if True shows 'problems not found' , 'no need to check this', 'problem found'  
