import psycopg2

def search_for_email(host, port, database, cluster, username, password, sql_query):

	try:

		result = ''

		DATABASE_URL="postgresql://{}:{}@{}:26257/{}.{}?sslmode=require".format(
			cockroachdb_username,
			cockroachdb_password,
			host,
			cockroachdb_cluster,
			database)

		conn = psycopg2.connect(DATABASE_URL)

		conn = psycopg2.connect(DATABASE_URL)		
		cur = conn.cursor()
		cur.execute(sql_query)
		rows = cur.fetchall()
		for row in rows:
			result += str(row) + '</br>'
		return (result, sql_query)
	except Exception as err:
		print(str(err))
		return (str(err), sql_query)


