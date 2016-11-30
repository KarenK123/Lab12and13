
from flask import Flask
import boto.sqs
import boto.sqs.message
from boto.sqs.message import Message

app = Flask(__name__)

@app.route("/listq")
def listq():
    qlist = []
    qliststring = ''
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    
    rs = conn.get_all_queues()
    for q in rs:
	qlist.append(q.id)

    qliststring = '<br/>'.join(qlist)
    return qliststring


@app.route("/deleteq/<username>", methods=['DELETE'])
def deleteq(username):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")

    try:
        q=conn.get_queue(username)

    except:
        return 'Failed to find queue ' + username

    try:
        conn.delete_queue(q,True)

        return username + ' queue has been deleted'

    except:
        return 'Could not delete the queue, or it does not exist'


@app.route("/createq/<username>")
def createq(username):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    
    try:
        q=conn.create_queue(username)
        return username + ' queue has been created or already exists'
    except:
        return 'Could not create queue. possible too soon since deletion, wait 60 seconds'

@app.route("/countq/<username>")
def countq(username):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    q = conn.get_queue(username)

    try:
        counter = q.counterr()
        return 'Messages in Queue = ' + counter
    except:
        return 'Could not read message'


@app.route("/writeq/<username>/<messg>")
def writeq(username, messg):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    m = Message()

    try:
        q=conn.get_queue(username)

    except:
        return 'Failed to find queue ' + username

    try:
        print messg
        m.set_body(messg)
        q.write(m)
        return messg + ' The message has been posted'

    except:
        return 'Could not write the message to queue, or queue does not exist'


@app.route("/consumeq/<username>")
def consumeq(username):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    q = conn.get_queue(username)

    try:
        m = Message()
        m = q.read(60)
        str1 = m.get_body()
        print "Message read = " + str1
    except:
        return 'Could not read message'
    try:
        q.delete_message(m)
        return 'message deleted from the queue'
    except:
        return 'Could not delete message'


@app.route("/readq/<username>")
def readq(username):
    conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id="AKIAJBPNKK2PQQPPU7PA", aws_secret_access_key="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")
    q = conn.get_queue(username)

    try:
        m = Message()
        m = q.read(60)
        str1 = m.get_body()

        return 'Message read = ' + str1

    except:
        return 'Could not read message'


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8888, debug=True)

