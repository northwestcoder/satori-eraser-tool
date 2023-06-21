import snowflake.connector

def search_for_email(host, database, snowflake_account, snowflake_username, snowflake_password, snowflake_warehouse, sql_query):
	
	try:
		result = ''

		ctx = snowflake.connector.connect(
			account=snowflake_account,
			password= snowflake_password,
			user=snowflake_username,
			host=host,
			warehouse=snowflake_warehouse,
			database=database
			)
		
		cs = ctx.cursor()			
		cs.execute(sql_query)
		for row in cs:
			result += str(row) + '</br>'
		return (result, sql_query)

	except Exception as err:
		print(str(err))
		return (str(err), sql_query)
