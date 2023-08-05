#!python
import os
import sys
import json
import argparse
import botocore
import boto3
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED

from sympy import ExactQuotientFailed

GB = 1024 ** 3
MULTIPART_THRESHOLD = GB/100
MAX_CONCURRENCY = 50

VISIBILITY_TIMEOUT = 3600
DELAY_SECONDS = 0

class Config:
    def __init__(self, path, file):
        self.path = path
        self.file = os.path.join(path,file)
        self.config = {}

        self.load()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.file, 'w') as config_file:
            json.dump(self.config, config_file)
        return

    def load(self):
        if os.path.isfile(self.file):
            with open(self.file) as config_file:
                self.config = json.load(config_file)
                return True
        else:
            return False            

    @property
    def region(self):
        return self.config.get('region', None)

    @region.setter
    def region(self, region):
        self.config['region'] = region

    @property
    def queue(self):
        return self.config.get('queue', None)

    @queue.setter
    def queue(self, queue):
        self.config['queue'] = queue

    @property
    def bucket(self):
        return self.config.get('bucket', None)

    @bucket.setter
    def bucket(self, bucket):
        self.config['bucket'] = bucket

    @property
    def prefix(self):
        return self.config.get('prefix', None)

    @prefix.setter
    def prefix(self, prefix):
        self.config['prefix'] = prefix

    @property
    def profile(self):
        return self.config.get('profile', None)

    @profile.setter
    def profile(self, profile):
        self.config['profile'] = profile

config = Config(os.path.join(os.path.expanduser('~'),'.s3copy'), 's3copy_config.json')


class Bucket:
    def __init__(self, session, bucket_name, prefix):
        self.s3 = session.client('s3')
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.config = TransferConfig(multipart_threshold = MULTIPART_THRESHOLD, 
                                     max_concurrency = MAX_CONCURRENCY)

        self.__create()
        self.put_lifecycle_configuration({
            'Rules': [{
                'Expiration': {
                    'Days':1
                },
                'ID':'s3copy',
                'Filter':{'Tag':{'Key':'s3copy','Value':'delete'}},
                'Status':'Enabled'
            }]
        })
        
    def __create(self):
        #Create bucket if it doesn't exist
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == '404':
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name)
                except botocore.exceptions.ClientError as error:
                    print(error)
            else:
                print(error)
            
    def put_lifecycle_configuration(self, lifecyle_configuration):
        try:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket = self.bucket_name,
                LifecycleConfiguration = lifecyle_configuration)
        except botocore.exceptions.ClientError as error:
            print(error)
        
    def upload_file(self, file_name):
        try:
            self.s3.upload_file(file_name, self.bucket_name, f'{self.prefix}/{file_name}', ExtraArgs={'Metadata':{'s3copy':'delete'}} ,Config = self.config)
        except botocore.exceptions.ClientError as error:
            print(error)

    def download_file(self, file_name):
        try:
            path = os.path.dirname(file_name)
            
            if len(path) > 0 and not os.path.exists(path):                
                os.makedirs(path)

            self.s3.download_file(self.bucket_name, f'{self.prefix}/{file_name}', file_name, Config = self.config)
        except botocore.exceptions.ClientError as error:
            print(error)

    def delete_file(self, file_name):
        try:
            self.s3.delete_object(Bucket = self.bucket_name, Key=f'{self.prefix}/{file_name}')
        except botocore.exceptions.ClientError as error:
            print(error)


class Queue:
    def __init__(self, session, queue_name):
        self.sqs = session.client('sqs')

        # Create queue if doesn't exist
        response = self.sqs.list_queues(QueueNamePrefix = queue_name) 
        if 'QueueUrls' not in response or len(response['QueueUrls'])==0:
            self.sqs.create_queue(QueueName = config.queue,
                                  Attributes = {
                                    "DelaySeconds": str(DELAY_SECONDS),
                                    "VisibilityTimeout": str(VISIBILITY_TIMEOUT)})

    def get_url(self):
        try:
            response = self.sqs.get_queue_url(QueueName = config.queue)
            return response["QueueUrl"]
        except botocore.exceptions.ClientError as error:
            print(error)

    def delete_message(self, receipt_handle):
        try:
            response = self.sqs.delete_message(
                QueueUrl = self.get_url(),
                ReceiptHandle=receipt_handle,
            )
        except botocore.exceptions.ClientError as error:
            print(error)
        
    def send_message(self, message):
        try:
            self.sqs.send_message(
                QueueUrl=self.get_url(),
                MessageBody=json.dumps(message))    
        except botocore.exceptions.ClientError as error:
            print(error)

    def receive_messages(self, fnc):
        def process_message(message, fnc):
            message_body = json.loads(message["Body"])
            fnc(message_body)                
            self.delete_message(message['ReceiptHandle'])

        try:
            response = self.sqs.receive_message(
                QueueUrl=self.get_url(),
                MaxNumberOfMessages=10,
                WaitTimeSeconds=5)

            num_messages = len(response.get('Messages', []))

            if num_messages > 0:
                pool = ThreadPoolExecutor()
                
                futures = []
                for message in response.get("Messages", []):
                    futures.append(pool.submit(process_message, message, fnc))
                
                wait(futures, timeout=None, return_when=ALL_COMPLETED)

                self.receive_messages(fnc)
        except botocore.exceptions.ClientError as error:
            print(error)

    
def init():
    if not config.load() or len(config.bucket)==0:
        print('Error: You first must configure the tool')
        sys.exit()

    try:
        session = boto3.Session(region_name = config.region,
                                profile_name = config.profile)

        bucket = Bucket(session, config.bucket, config.prefix)
        queue = Queue(session, config.queue)
    
    except botocore.exceptions.ProfileNotFound as error:
        if config.profile == 'default':
            session = boto3.Session(region_name = config.region)

            bucket = Bucket(session, config.bucket, config.prefix)
            queue = Queue(session, config.queue)
        else:
            print(error)
            sys.exit()

    return bucket, queue

def send_files(**args):
    bucket, queue = init()
    def send_file(bucket, queue, file_name):
        bucket.upload_file(file_name)
        message = {'file': file_name}
        queue.send_message(message)
        return f'{file_name} sent'         

    
    futures = {}
    with ThreadPoolExecutor() as executor:
        for path in args['files']:
            if os.path.isfile(path):                
                futures[executor.submit(send_file, bucket, queue, path)] = path
            elif os.path.isdir(path):        
                for (root,dirs,files) in os.walk(path, topdown=True):
                    for file in files:                        
                        file_path = os.path.join(root,file)
                        futures[executor.submit(send_file, bucket, queue, file_path)] = file_path
            else:
                print('File not found or not supported')

        wait(futures, timeout=None, return_when=ALL_COMPLETED)
        for future in as_completed(futures):
            path = futures[future]
            try: 
                result = future.result()
            except Exception as error:
                print(f'{path} generated an exception')
                print(error)
            else:
                print(f'{result}')
    

def receive_files():
    bucket, queue = init()

    def process_message(message_body):        
        file_name = message_body['file']        
        bucket.download_file(file_name)      
        print(f"{file_name} downloaded")  
        bucket.delete_file(file_name)

    queue.receive_messages(process_message)

def configure():
    parameters = {
        'region': 'us-east-1',
        'queue': 's3copy',
        'bucket': '',
        'prefix': 's3copy',
        'profile': 'default'}
    
    for param in parameters:
        attr = getattr(config, param, None) 
        val = attr if attr != None else parameters[param]
        setattr(config, param, input(f'{param} [{val}]: ') or val)
    
    config.save()

def invalid_command():
    raise Exception('Invalid action')

def command_selector(command, **args):    
    commands = {
        'configure': configure, 
        'send': send_files,
        'receive': receive_files}

    command_fnc = commands.get(command, invalid_command)

    return command_fnc(**args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Tool to copy files using Amazon S3.',
        epilog="Don't forget to configure it before using it")

    subparsers = parser.add_subparsers(title='actions to perform', dest='command')

    configure_parser = subparsers.add_parser('configure', help='set the configuration parameters.')

    send_parser = subparsers.add_parser('send', help='send files')
    send_parser.add_argument(nargs='+', dest='files')

    receive_parser = subparsers.add_parser('receive', help='receive files')

    args = parser.parse_args()    


    if args.command==None:        
        parser.print_help()

    else:
        command_selector(**vars(args))    
