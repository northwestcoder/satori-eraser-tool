import mysql.connector

def search_for_email(host, port, database, location, user, password, email_to_find, colname):

	str_sql = "SELECT * from {} where {} = '{}';".format(location, colname, email_to_find)

	try:

		result = ''
		mysql_con = mysql.connector.connect(
			user=user,
			password=password,
			host=host,
			database=database,
			port=port)

		mycursor = mysql_con.cursor()

		mycursor.execute(str_sql)

		rows = mycursor.fetchall()
		for row in rows:
			result += str(row) + '</br>'
		return (result, str_sql)

	except Exception as err:
		print(err)
		return (str(err), str_sql)