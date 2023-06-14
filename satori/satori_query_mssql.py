import pyodbc

def search_for_email(host, database, user, password, sql_query):

	try:
		result = ''
		cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+host+';DATABASE='+database+';ENCRYPT=yes;UID='+user+';PWD='+ password)
		cursor = cnxn.cursor()
		cursor.execute(sql_query) 
		rows = cursor.fetchall()
		for row in rows:
			result += str(row) + '</br>'
		return (result, sql_query)
	except Exception as err:
		print(err)
		return (str(err),sql_query)
