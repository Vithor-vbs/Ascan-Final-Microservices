
import pika, json
import django
django.setup()

from core.models import Comment

params = pika.URLParameters('amqps://vddjqqjj:jcCZzfXmZA0FbJLBsw6GoxQIZIc3txd2@sparrow.rmq.cloudamqp.com/vddjqqjj')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in posts')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'post_created':
        comment = Comment(text=data['text'], post_id=data['post_id'])
        comment.save(using='comments_db')
        print('Comment Created')

    elif properties.content_type == 'post_deleted':
        comment = Comment.objects.get(post_id=data['post_id'])
        comment.delete(using='comments_db')
        print('Comment Deleted')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()