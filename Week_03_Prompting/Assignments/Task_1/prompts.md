APE:

ACTION:
Read the natural language queries in the attached file restaurants_dataset.csv. For each query, write the SQL query that answers it. Use the database schema in restaurants-schema.csv and the database contents in restaurants-db.txt. Produce a CSV file with two columns: the first contains the natural language query, the second contains the matching SQL query.

PURPOSE:
The CSV will be used as a reference set of natural-language-to-SQL pairs. Every SQL query must be correct and executable against this exact database, because the pairs will be used to check whether questions are translated into SQL accurately.

EXPECTATION:
- Output only the CSV content, with no explanations before or after it.
- Header row: natural_text,sql_query
- One row per natural language query, in the same order as in restaurants_dataset.csv. Copy the natural language text exactly, without rewording it.
- Enclose both fields in double quotes and escape any double quotes inside a field by doubling them ("").
- Write each SQL query on a single line, ending with a semicolon.
- Use only tables and columns that exist in restaurants-schema.csv.
- Use restaurants-db.txt to check exact values, such as the spelling and capitalization of names, cities, and categories.
- Use [SQL DIALECT] syntax.
- If a query is ambiguous, choose the most reasonable interpretation and do not add comments.


ERA:

EXPECTATION:
I expect a CSV file with exactly two columns and the header natural_text,sql_query. The first column contains each natural language query from restaurants_dataset.csv, copied exactly and in the original order. The second column contains a correct, executable [SQL DIALECT] query that answers it. Enclose both fields in double quotes and escape inner double quotes as "". Write each SQL query on one line, ending with a semicolon. Output only the CSV content, with no explanations.

ROLE:
You are an experienced database engineer and SQL expert who specializes in translating natural language questions into precise SQL queries. You are careful about table relationships, joins, aggregations, filtering, and exact data values.

ACTION:
1. Study the database schema in restaurants-schema.csv: tables, columns, data types, and keys.
2. Review the data in restaurants-db.txt to learn the exact values stored, such as the spelling and capitalization of names, cities, and categories.
3. Go through restaurants_dataset.csv one query at a time and write the SQL query that answers it, using only tables and columns that exist in the schema.
4. If a query is ambiguous, choose the most reasonable interpretation without adding comments.
5. Assemble all pairs into the CSV described above.


CRISP:

CONTEXT:
I have a restaurant database. Its structure is described in restaurants-schema.csv and its contents are in restaurants-db.txt. The file restaurants_dataset.csv contains natural language questions about this database. I need each question paired with the SQL query that answers it.

ROLE:
Act as an experienced database engineer and SQL expert who translates natural language questions into precise, executable SQL queries.

INSTRUCTIONS:
1. Read the schema and identify all tables, columns, data types, and relationships between tables.
2. Review the database contents to learn the exact values stored.
3. For each natural language query in restaurants_dataset.csv, write the SQL query that answers it.
4. Output the results as a CSV file with two columns: the natural language query and the SQL query.

SPECIFICS:
- Use only tables and columns that exist in restaurants-schema.csv.
- Match exact values from restaurants-db.txt, including the spelling and capitalization of names, cities, and categories.
- Copy the natural language text exactly, without rewording it, and keep the original order of the queries.
- If a query is ambiguous, choose the most reasonable interpretation and do not add comments.

PARAMETERS:
- SQL dialect: [SQL DIALECT]
- Header row: natural_text,sql_query
- One row per query. Enclose both fields in double quotes and escape inner double quotes as "".
- Each SQL query on a single line, ending with a semicolon.
- Output only the CSV content, with no text before or after it.