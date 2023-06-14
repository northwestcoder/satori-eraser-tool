# Satori Opt-Out CLI and Report Builder

<img src="https://satoricyber.com/wp-content/uploads/LogoDark2.svg" />

_A command line driven experience to search across all Satori datastores for any TAG with any SEARCH_STRING and generate a web report with the results_

### Supported Database Types

- PostgreSQL (with Satori credentials)
- MySQL (with Satori credentials)
- MSSQL (with Satori credentials)
- Snowflake
- Athena (with Satori credentials)
- Redshift (with Satori credentials)
- CockroachDB 

### Installation

- At a command prompt, download this repo, navigate to the new repo directory and then
```pip install -r requirements.txt```
- Fill out values in satori/satori.py
- If not using Snowflake, Athena, or CockroachDB, you can leave those lines alone
- Satori [username and temp credentials](https://satoricyber.com/docs/data%20portal/#data-store-temporary-credentials) are required for Athena, Postgres, MySQL, Redshift and MSSQL. You can also place original database username and password into these values.

_We strongly recommend using a virtual python environment!_


### Usage

_This tool uses an async python process and javascript in the web browser (flask and socketIO) to retrieve results from various queries performed by this tool. When you load the web page, it should start to populate with search results automatically. When you are finished, close the web page to end the async session!_

The premise is:

- That you fire up the command line tool, and then navigate to http://127.0.0.1:8080/ to trigger the generation of a report. 
- When the report is finished, it will show "Finished querying all Satori datastore locations" at the top of the web page. 
- Copy the contents of the web page or print to PDF.
- Close the web page to end communication with the command line tool.
- You can then ctrl-C the command line tool to halt the process or perform a new query.

To start the tool, the syntax is like:

```%>python app.py TAGNAME SEARCH_STRING ```

Where:

- TAGNAME is a valid [Satori Data Inventory](https://satoricyber.com/docs/inventory/) tag, e.g. SSN or EMAIL or CITY, etc.
- SEARCH_STRING is the value you want to search for across all Satori Datastores

The results are divided into two sections:

1. We show each location for TAG, and any results from the database for that TAG where value = SEARCH_STRING.
2. We then list select statements for each location for TAG, this is for a data engineer to perform additional research or exploration.

##### Examples

```
%>python app.py SSN 322-87-9857
%>python app.py EMAIL svega674@lewisramirezandstephenson.biz
%>python app.py ALLERGIES "J30.9 Allergic rhinitis  unspecified"
%>python app.py STATE OR
%>python app.py CITY Comanche 
```

You can also use [Satori Custom Inventory](https://satoricyber.com/docs/inventory/#custom-data-classification), but you will need to know its internal ID (available in the URL when looking at your custom inventory classifier), e.g. if you have a custom tag for emails, you could search like:

```
%>python app.py eec10645-6358-48eb-a5e3-6af917600b0a svega674@lewisramirezandstephenson.biz
```


