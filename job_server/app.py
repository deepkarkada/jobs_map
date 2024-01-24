import os
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

## Using SQLAlchemy to read from the database 
## Ref: https://pythondata.com/quick-tip-sqlalchemy-for-mysql-and-pandas/
connect_string = f'mysql://{USER}:{PW}@{HOST}:{PORT}/{DB}'
sql_engine = sql.create_engine(connect_string)
query = "SELECT * FROM jobs"
jobs_df = pd.read_sql_query(query, sql_engine)

from openai import OpenAI 

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()

def get_response(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': f'Based on the context provided in the text delimited by triple backticks, produce the technologies used in the context as a python list. The context provided is: ```{text}```' }
        ]
    )
    return response.choices[0].message.content

with gr.Blocks() as demo:
    with gr.Row():
            gr.Markdown("Company")
            gr.Markdown("Job title")
            gr.Markdown("Job description")
            gr.Markdown("Tasks")
    for index, row in jobs_df.iterrows():
        #gr.Row(fn=greet, inputs=gr.Checkbox(label=row['description']), outputs=gr.Radio(["park", "zoo", "road"], label="tasks"))
        with gr.Row():
            gr.Markdown(f"{row['company']}")
            gr.Markdown(f"{row['title']}")
            gr.Markdown(f"{row['description']}")
            responses = get_response(row['description'])
            responses = responses.split(']')[0].split('[')[-1].split(',')
            #print(f'Response: {responses}')
            gr.Radio(choices=[response.lstrip("'").rstrip("'") for response in responses], label="tasks")
        
        ## For testing purposes
        if index == 2:
             break

demo.launch(server_name="0.0.0.0", server_port=5004)