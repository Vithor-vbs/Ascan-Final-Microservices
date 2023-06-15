
import pika, json
import django
django.setup()

from core.models import Comment


params = pika.URLParameters('amqps://vddjqqjj:jcCZzfXmZA0FbJLBsw6GoxQIZIc3txd2@sparrow.rmq.cloudamqp.com/vddjqqjj')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Received in comments')
    data = json.loads(body)
    print(data) 

    if properties.content_type == 'post_created':
        
        print('Post Created')

    elif properties.content_type == 'post_updated':
        
        print('Post Updated')

    elif properties.content_type == 'post_deleted':
        
        print('Post Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()