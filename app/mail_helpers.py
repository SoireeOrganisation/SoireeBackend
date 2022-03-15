from flask_mail import Mail, Message


mail = Mail()


def send_message(topic, body, email):
    with mail.app.app_context():
        try:
            msg = Message(topic,
                          sender='soiree.app@list.ru',
                          recipients=[email])
            msg.body = body
            mail.send(msg)
        except Exception as e:
            print(e)

