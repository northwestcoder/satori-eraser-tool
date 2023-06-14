import mysql.connector

def search_for_email(host, port, database, user, password, sql_query):

	try:

		result = ''
		mysql_con = mysql.connector.connect(
			user=user,
			password=password,
			host=host,
			database=database,
			port=port)

		mycursor = mysql_con.cursor()

		mycursor.execute(sql_query)

		rows = mycursor.fetchall()
		for row in rows:
			result += str(row) + '</br>'
		return (result, sql_query)

	except Exception as err:
		print(err)
		return (str(err), sql_query)