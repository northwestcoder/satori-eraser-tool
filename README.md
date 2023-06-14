# Satori GDPR/CCPA Opt-Out CLI and Report Builder

<img src="https://satoricyber.com/wp-content/uploads/LogoDark2.svg" />

_A command-line -driven experience to search across all Satori datastores for any TAG with any SEARCH_STRING and generate a web report with the results_

### Supported Database Types

- PostgreSQL
- MySQL
- MSSQL
- Snowflake
- Athena
- Redshift
- CockroachDB 

### Installation

_Due to several python libraries installed for various databases, we strongly recommend using a virtual python environment!_

We tested using [pyenv on a mac](https://github.com/pyenv/pyenv#homebrew-in-macos) with python 3.11.0. 

The rest of these installation steps assume you have a dedicated and clean (and hopefully virtual) python environment:

- At a command prompt, download this repo, navigate to the new repo directory and then:
```
pip install -r requirements.txt
```
- Fill out values in [satori/satori.py](https://github.com/northwestcoder/satori-gdpr-async/blob/main/satori/satori.py)
	- This solution requires a [Satori API service ID and Key](https://app.satoricyber.com/docs/api).
	- If you are not using Snowflake, Athena, or CockroachDB, you can leave these lines alone.
	- Satori [username and temp credentials](https://satoricyber.com/docs/data%20portal/#data-store-temporary-credentials) can be used for Athena, Postgres, MySQL, Redshift and MSSQL.
	- Or, you can use original database username and password for these variables. 
	- Snowflake and CockroachDB will require database username and password.

### Usage

_This tool uses an async python process and javascript in the web browser (flask and socketIO) to retrieve results from various queries performed by this tool. When you load the web page, it should start to populate with search results automatically. When you are finished, close the web page to end the async session!_

The premise is:

- That you fire up the command line tool, and then navigate to http://127.0.0.1:8080/ to trigger the generation of a report. 
- When the report is finished, it will show "Finished querying all Satori datastore locations" at the top of the web page. 
- Copy the contents of the web page or print to PDF.
- Close the web page to end communication with the command line tool.
- You can then ctrl-C the command line tool to halt the process or perform a new query.

To start the tool, the syntax is like:

```python app.py TAGNAME SEARCH_STRING ```

Where:

- required: **TAGNAME** is a valid [Satori Data Inventory](https://satoricyber.com/docs/inventory/) tag, e.g. SSN, EMAIL, CITY, etc.
- required: **SEARCH_STRING** is the value you want to search for across all Satori Datastores. Use quotes for a search string with spaces.

The results are divided into two sections:

1. We show each location for TAG, and any results from the database for that TAG where value = SEARCH_STRING.
	- Note: This tool makes a simple attempt at pretty-printing with a new line for each row returned.
2. We then list SQL select statements for each location for TAG.
	- This is for a data engineer to perform additional research or exploration.

##### Examples

```
python app.py SSN 322-87-9857
python app.py EMAIL svega674@lewisramirezandstephenson.biz
python app.py ALLERGIES "J30.9 Allergic rhinitis  unspecified"
python app.py STATE "Oregon"
python app.py CITY "San Francisco" 
```

You can also use [Satori Custom Inventory](https://satoricyber.com/docs/inventory/#custom-data-classification), but you will need to know its internal ID (available in the URL when looking at your custom inventory classifier), e.g. if you have a custom tag for emails, you could search like:

```
python app.py eec10645-6358-48eb-a5e3-6af917600b0a svega674@lewisramirezandstephenson.biz
```
