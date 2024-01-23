import gradio as gr
import pandas as pd
import sqlalchemy as sql

## toy implementation to see gradio is working
# def greet(name, intensity):
#     return "Hello " * intensity + name + "!"

# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", "slider"],
#     outputs=["text"],
# )

# demo.launch(server_name="0.0.0.0", server_port=5003)

## sql config
mysql_config = {
    'host': 'jobs_map-db-1',
    'port': 3306,
    'user': 'root',
    'pw': "",
    'db': 'jobsdb'
}

USER = mysql_config['user']
HOST = mysql_config['host']
PORT = mysql_config['port']
PW = mysql_config['pw']
DB = mysql_config['db']

# connection_string = f"mysql://{USER}:{PW}@{HOST}:{PORT}/{DB}"

# def get_jobs():
#     df = pd.read_sql(
#         """
#     SELECT * FROM jobs
#     """,
#     con=connection_string
#     )


# import mysql.connector


# mydb = mysql.connector.connect(
#     host = HOST,
#     port = PORT,
#     user = USER,
#     database = DB
# )

# query = "SELECT * FROM jobs"
# jobs_df = pd.read_sql_query(query, mydb)
# jobs_df = jobs_df.to_json()

## Using SQLAlchemy to read from the database 
## Ref: https://pythondata.com/quick-tip-sqlalchemy-for-mysql-and-pandas/
connect_string = f'mysql://{USER}:{PW}@{HOST}:{PORT}/{DB}'
sql_engine = sql.create_engine(connect_string)
query = "SELECT * FROM jobs"
jobs_df = pd.read_sql_query(query, sql_engine)
#print(f'Jobs: {jobs_df.head()}')
#jobs_df = jobs_df.to_json()

# with gr.Blocks() as demo:
#     gr.DataFrame(jobs_df)

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    for index, row in jobs_df.iterrows():
        #with gr.Row():
        gr.Row(fn=greet, inputs=gr.Checkbox(label=row['description']), outputs=gr.Radio(["park", "zoo", "road"], label="tasks"))

demo.launch(server_name="0.0.0.0", server_port=5004)