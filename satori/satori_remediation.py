def build_remediation(search_results, query_location, column_name, email_to_find):

	remediation = "delete from " + query_location + " where " + column_name + " = '" + email_to_find + "';"

	return remediation
									