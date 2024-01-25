import os
import pika
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


## Ref: https://dhruvadave5297.medium.com/demo-application-for-background-processing-with-rabbitmq-python-flask-c3402bdcf7f0

def add_task(task):
    task = task['label']
    print(f'Rabbitmq got input: {task}')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=task,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
   
    connection.close()
    print(f'__Sent task: {task} to rabbitmq queue')
    #return f" ___ Sent: {task}"

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
            #gr.Radio(choices=[response.lstrip("'").rstrip("'") for response in responses], label="tasks").input(add_task)
            for i, response in enumerate(responses):
                response = response.strip("'")
                #btn = gr.Button(f'{response}', label=f"tasks_{i}")
                # btn = gr.Button(f'{response}')
                # btn.click(add_task, inputs=[response], outputs=[])
                
                # radio = gr.Radio(choices=[response.strip("'")], value=None, label=f"tasks_{i}")
                # radio.change(add_task, radio, outputs=[])
                tsk = gr.Label(label=response, value=response, visible=False)
                chkbx = gr.Checkbox(label=[response], value=None)
                chkbx.select(add_task, tsk, outputs=[])
        
        ## For testing purposes
        if index == 2:
             break

demo.launch(server_name="0.0.0.0", server_port=5004)