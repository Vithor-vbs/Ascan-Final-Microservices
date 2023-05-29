
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

    if properties.content_type == 'comment_created':
        comment = Comment(id=data['id'], text=data['text'], post_id=data['post_id'])
        comment.save()
        print('Comment Created')

    elif properties.content_type == 'comment_updated':
        comment = Comment.objects.get(id=data['id'])
        comment.text = data['text']
        comment.save()
        print('Comment Updated')

    elif properties.content_type == 'comment_deleted':
        comment = Comment.objects.get(id=data['id'])
        comment.delete()
        print('Comment Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()