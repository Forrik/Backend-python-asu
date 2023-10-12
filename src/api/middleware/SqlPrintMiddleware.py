from django.db import connection


class SqlPrintMiddleware(object):
    def process_response(self, request, response):
        sqltime = 0 # Variable to store execution time
        for query in connection.queries:
            sqltime += float(query["time"])  # Add the time that the query took to the total
 
        # len(connection.queries) = total number of queries
        print(f"Page render: {sqltime} sec for {len(connection.queries)} queries")
 
        return response