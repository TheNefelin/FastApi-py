import pymssql
# import psycopg2
import os

conn = pymssql.connect(
  user = os.getenv("MSSQL_USER"), 
  server = os.getenv("MSSQL_HOST"),
  password = os.getenv("MSSQL_PASSWORD"),
  database = os.getenv("MSSQL_DATABASE")
)

# conn = psycopg2.connect(
#   user = os.getenv("POSTGRES_USER"),
#   host = os.getenv("POSTGRES_HOST"),
#   password = os.getenv("POSTGRES_PASSWORD"),
#   database = os.getenv("POSTGRES_DATABASE"),
#   port="5432"
# )

async def execute_query(query):
  try:
    with conn.cursor() as cursor:
      cursor.execute(query)
      result = cursor.fetchall()
      conn.commit()
      return result
  except Exception as ex:
    return [{"estado": False, "error": str(ex)}]
  
async def execute_sp(sp, params):
  try:
    with conn.cursor(as_dict = True) as cursor:
      cursor.callproc(sp, params)
      result = cursor.fetchall()
      conn.commit() # important for insert update delete
      return result
  except Exception as ex:
    return [{"estado": False, "error": str(ex)}]

