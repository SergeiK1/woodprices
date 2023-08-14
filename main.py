import tabula 




# Reading PDF and converting to usable data __________________________________________

# Installed java

pdf_path = 'testfile.pdf'
dfs = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

print(dfs)


# Uplaoding this data into a seperate file to act as a database for the historical data _____________________________
# Make upon uploading the first pdf in make a file that acts as a database (simple text file named databse.txt)
# Then updates this database with all the value for each wood type every entery 




# Then take all those data points over the course of multiple entries all on the database.txt and extracts it with a simple file read__________________
# Then take all those values and displays a chart for each type with this historic data 







# Possible additional functionality ____________________________
# adds checks to see if price rose or dropped and make the chart different colors (green red) and make that able to be manipulated by the user 








