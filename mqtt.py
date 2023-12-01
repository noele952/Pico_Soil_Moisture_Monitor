from umqtt.simple import MQTTClient
import time
import ujson


class MQTT:
    def __init__(self, machine_id, endpoint, client_id, topic_pub, topic_sub=None):
        # Initialize MQTT object
        self.machine_id = machine_id
        self.cert_file = 'certs/certificate.der'
        self.key_file = 'certs/private.der'
        self.endpoint = endpoint
        self.client_id = client_id
        self.topic_pub = topic_pub
        self.topic_sub = topic_sub
        self.port = 8883
        self.keepalive = 3600
        self.max_retries = 3
        self.client = self.connect_client()


    def connect_client(self):
        # Connect to the MQTT broker with SSL/TLS
        retry_count = 0
        with open(self.cert_file, 'rb') as f:
            cert = f.read()
            
        with open(self.key_file, 'rb') as f:
            key = f.read()

        print("Key and Certificate files Loaded")
        SSL_PARAMS = {'key': key, 'cert': cert, 'server_side': False}
        while retry_count < self.max_retries:
            try:
                client = MQTTClient(self.client_id, self.endpoint, port=self.port, keepalive=self.keepalive, ssl=True, ssl_params=SSL_PARAMS)
                client.connect()
                print('Connected to %s MQTT Broker' % (self.endpoint))
                return client
            except OSError as e:
                print(e)
                print('Failed to connect to the MQTT Broker. Retrying...')
                retry_count += 1
                time.sleep(5)

        print('Failed to connect to the MQTT Broker after {self.max_retries} attempts.')
        return None


    def post(self, label, data):
        # Publish data to MQTT broker
        try:
            message = ujson.dumps({ 'machine_id': self.machine_id,
                                    'label' : 'data',
                                    'type' : label,
                                    'value': data })
            self.client.publish(self.topic_pub, message)
        except Exception as error:
            print("An error occurred:", error)


    def mqtt_callback(self, topic, msg):
        # Handle incoming MQTT messages
        print("New message on topic {}".format(topic.decode('utf-8')))
        message = msg.decode('utf-8')
        print(message)
