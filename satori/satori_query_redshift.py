import psycopg2

def search_for_email(host, port, database, location, user, password, email_to_find, colname):

	str_sql = "SELECT * from {} where {} = '{}';".format(location, colname, email_to_find)
	result = ''

	try:
		connector: psycopg2.connection = psycopg2.connect(
				database=database, user=user, password=password, host=host, port=port, sslmode='require'
			)
	except Exception as err:
		print(err)
		return (str(err), str_sql)
	else:
		cur = connector.cursor()

	try:
		cur.execute(str_sql)
	except Exception as err:
		print(err)
		connector.rollback()
		return (str(err), str_sql)
	
	try:
		rows = cur.fetchall()
		for row in rows:
			result += str(row) + '</br>'
	except Exception as err:
		print(err)
		connector.rollback()
		return (str(err), str_sql)
	else:
		connector.commit()
		return (result, str_sql)