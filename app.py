import sys
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from threading import Thread, Event
from collections import defaultdict

from satori import satori
from satori import satori_common
from satori import satori_locations as locations
from satori import satori_datastores as datastores
from satori import satori_remediation as remediation

#db clients
from satori import satori_query_postgres as postgres
from satori import satori_query_mysql as mysql
from satori import satori_query_mssql as mssql
from satori import satori_query_athena as athena
from satori import satori_query_cockroach as cockroachdb
from satori import satori_query_redshift as redshift
from satori import satori_query_snowflake as snowflake

# change your ports as needed. Snowflake and Athena do not require ports
PORT_POSTGRES = "5432"
PORT_REDSHIFT = "5439"
PORT_COCKROACH = "26257"
PORT_MYSQL = "12343"

app = Flask(__name__)
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

search_string = ''
satori_tag = ''

satori_account_id = satori.satori_account_id 
satori_serviceaccount_id = satori. satori_serviceaccount_id 
satori_serviceaccount_key = satori.satori_serviceaccount_key
apihost = satori.apihost
print("using api server: " + apihost)
satori_username = satori.satori_username
satori_password = satori.satori_password
snowflake_username = satori.snowflake_username
snowflake_password = satori.snowflake_password
snowflake_account = satori.snowflake_account
cockroachdb_username = satori.cockroachdb_username
cockroachdb_password = satori.cockroachdb_password
cockroachdb_cluster = satori.cockroachdb_cluster
athena_results = satori.athena_results
athena_region = satori.athena_region

def async_get_datastores():

    query_items = defaultdict(list)
    satori_token = satori_common.satori_auth(satori_serviceaccount_id, satori_serviceaccount_key, apihost)

    auth_headers = {
    'Authorization': 'Bearer {}'.format(satori_token), 
    'Content-Type': 'application/json', 'Accept': 'application/json'
    }

    found_datastores = datastores.get_all_datastores(
        auth_headers, 
        apihost, 
        satori_account_id)

    for ds_entry in found_datastores[1]:

        ds_name = ds_entry['name']
        datastore_id = ds_entry['id']
        satori_hostname = ds_entry['satoriHostname']
        satori_displayname = ds_entry['name']
        db_type = ds_entry['type']

        socketio.emit('SatoriResults', 
            {'SearchResults': '<b>' + ds_name + '</b></br>'},
            namespace='/test')

        found_locations = locations.get_locations_by_datastore(auth_headers, 
                                                               apihost, 
                                                               satori_account_id, 
                                                               datastore_id)

        print("\nSearching " + str(found_locations[0]) + " locations for datastore " + satori_hostname + " (" + db_type + ")")
        
        for location_entry in found_locations[1]:

            #reset the search results after each location
            search_results = ['','']
            remediation_response = ''

            tags = location_entry['tags']
            if tags is not None:
                for tag_item in tags:
                    if tag_item['name'] == satori_tag:

                        # for each location of type EMAIL, we build the following vars:
                        # dbname, table, column_name, schema, query-able location, full_location

                        # Need to finish databricks, for now omitting
                        if db_type == 'DATABRICKS':
                            dbname =        ''
                            table =         ''
                            column_name =   ''
                        else:
                            dbname =        location_entry['location']['db']
                            table =         location_entry['location']['table']
                            column_name =   location_entry['location']['column']
                            #some DB's don't have a concept of schema
                            if db_type in ('MARIA_DB', 'ATHENA', 'MYSQL'):
                                schema = ''
                                query_location = table
                                full_location = satori_hostname + '::' + dbname + '.' + table + '.' + column_name
                            else:
                                schema = location_entry['location']['schema']
                                query_location = schema + '.' + table
                                full_location = satori_hostname + '::' + dbname + '.' + schema + '.' + table + '.' + column_name


                        sql_query = "SELECT * from {} where {} = '{}';".format(query_location, column_name, search_string)

                        # BEGIN MAIN DB CLIENT WORK

                        if db_type == 'POSTGRESQL' and satori_username != '':
                            search_results = postgres.search_for_email(
                                satori_hostname, 
                                PORT_POSTGRES, 
                                dbname, 
                                satori_username, 
                                satori_password, 
                                sql_query)

                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )

                            query_items[satori_hostname + "::" + dbname].append(search_results[1])

                        if db_type == 'MYSQL' and satori_username != '':
                            search_results = mysql.search_for_email(
                                satori_hostname, 
                                PORT_MYSQL, 
                                dbname, 
                                satori_username, 
                                satori_password, 
                                sql_query)

                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )

                            query_items[satori_hostname + "::" + dbname].append(search_results[1])
                        
                        if db_type == 'REDSHIFT' and satori_username != '':
                            search_results = redshift.search_for_email(
                                satori_hostname, 
                                PORT_REDSHIFT, 
                                dbname, 
                                satori_username, 
                                satori_password, 
                                sql_query)

                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )

                            query_items[satori_hostname + "::" + dbname].append(search_results[1])
                        
                        if db_type == 'MSSQL' and satori_username != '':
                            search_results = mssql.search_for_email(
                                satori_hostname,
                                dbname,
                                satori_username,
                                satori_password,
                                sql_query)
                            
                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )
                    
                            query_items[satori_hostname + "::" + dbname].append(search_results[1])

                        if db_type == 'ATHENA' and athena_results != '':
                            search_results = athena.search_for_email(
                                athena_results,
                                athena_region,
                                satori_hostname,
                                dbname,
                                satori_username,
                                satori_password,
                                sql_query)
                            
                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )
  
                            query_items[satori_hostname + "::" + dbname].append(search_results[1])

                        if db_type == 'COCKROACH_DB' and cockroachdb_username != '':
                            search_results = cockroachdb.search_for_email(
                                satori_hostname,
                                PORT_COCKROACH,
                                dbname,
                                cockroachdb_cluster,
                                cockroachdb_username, 
                                cockroachdb_password, 
                                sql_query)
                            
                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )
 
                            query_items[satori_hostname + "::" + dbname].append(search_results[1])

                        if db_type == 'SNOWFLAKE' and snowflake_username != '':
                            search_results = snowflake.search_for_email(
                                satori_hostname,
                                dbname,
                                snowflake_account,
                                snowflake_username,
                                snowflake_password,
                                sql_query
                                )

                            remediation_response = remediation.build_remediation(
                                query_location, 
                                column_name, 
                                search_string
                                )

                            query_items[satori_hostname + "::" + dbname].append(search_results[1])

                        socketio.emit('SatoriResults', 
                                {'SearchResults': '<i>' + full_location + '</i></br><div class="resultsindent"><b>Results:</b></br>' + search_results[0] + '</br></br><b>Remediation:</b></br>' + remediation_response + '</div></br>'},
                                namespace='/test')

    queries_formatted = ''
    for location, queries in query_items.items():
        queries_formatted += '</br><b>' + location.split("::")[0] + '</b></br>'
        for item in queries:
            queries_formatted += '<div class="resultsindent">' + str(item) + '</div>'

    socketio.emit('QueryInfo', 
    {'Queries': queries_formatted},
    namespace='/test')

    socketio.emit('Completion', 
    {'Complete': "Finished querying all Satori Datastore <b>" + satori_tag + "</b> locations for value <b>" + search_string + "</b>"},
    namespace='/test')


@app.route('/', methods=['GET'])
def results():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.is_alive():
        print("Starting Threads")
        thread_datastores = socketio.start_background_task(async_get_datastores)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':

    satori_tag = sys.argv[1]
    search_string = sys.argv[2] 
    socketio.run(app, host='127.0.0.1', port=8080)
