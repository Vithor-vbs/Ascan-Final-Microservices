import pika, json

params = pika.URLParameters('amqps://vddjqqjj:jcCZzfXmZA0FbJLBsw6GoxQIZIc3txd2@sparrow.rmq.cloudamqp.com/vddjqqjj')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)