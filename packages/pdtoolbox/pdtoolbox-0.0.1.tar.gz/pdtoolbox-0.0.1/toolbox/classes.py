import pika
import json


class Consumer(object):

    def __init__(self, rmq_credentials, rmq_host, rmq_hb):
        """
        initiation method to connect to rabbit, execute run() to start worker

        :param rmq_credentials: rabbit credentials object for connecting
        :param rmq_host: host address
        :param rmq_hb: rabbit heartbeat interval
        """
        # rabbit connection
        self.rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rmq_host, port=5672, virtual_host='/', credentials=rmq_credentials, heartbeat=rmq_hb))
        self.channel = None

    def run(self, rmq_exchange, rmq_queue='', rmq_ex_type='fanout', rmq_queue_exclusive=True, rmq_auto_ack=True,
            rmq_prefetch_count=0):
        """
        Function to run to start the consumer obtaining data from the rabbit queue / exchange

        :param rmq_exchange: name of exchange to connect to, must have
        :param rmq_queue: name of exchange to connect to, if a persistent queue then name it
        :param rmq_ex_type: the type of exchange it connects to, default is 'fanout'
        :param rmq_queue_exclusive: boolean to define is the queue is exclusive (true),
                                    i.e. only one consumer can connect. Default is True
        :param rmq_auto_ack: boolean to define if the queue should auto acknowledge message received.
                             Default it True for performance reasons (True cannot be used with
                             channel.basic_ack() in callback)
        :param rmq_prefetch_count: is the number of message the consumer will take from the queue at a time.
                                   Default is 0, i.e. take all the messages (unlimited)
        :return: n/a
        """

        # open up channel and exchange
        print('|| open up channel ||')
        self.channel = self.rmq_connection.channel()
        self.channel.exchange_declare(exchange=rmq_exchange, exchange_type=rmq_ex_type)

        # set the quality of service
        print('|| Setup up QoS on channel, prefetch count ' + str(rmq_prefetch_count) + ' ||')
        self.channel.basic_qos(prefetch_count=rmq_prefetch_count)

        # create queue which is connected to exchange
        result = self.channel.queue_declare(queue=rmq_queue, exclusive=rmq_queue_exclusive)
        queue_name = result.method.queue
        print('|| Queue declare ' + str(queue_name) + ' ||')
        self.channel.queue_bind(queue=queue_name, exchange=rmq_exchange)

        # start consuming messages
        print('|| Start Consuming ||')
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=rmq_auto_ack)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body: json):
        """
        needs to be defined for each used of the parent class
        """
        None
