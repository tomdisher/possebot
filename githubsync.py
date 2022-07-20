import boto3
import git
import os,sys,time
from daemonize import Daemonize
local_path='/path/to/git/dir'
def main():
    while True:
        sqs = boto3.resource('sqs',
                    aws_access_key_id="<key id>",
            aws_secret_access_key="<secret key>",
            region_name='us-east-1')
        
        
        # Send message to SQS queue
        queue = sqs.get_queue_by_name(QueueName='queue_name_not_arn')
        
        # Process messages by printing out body and optional author name
        messages =queue.receive_messages()
            # Get the custom author message attribute if it was set
        
            # Print out the body and author (if set)
        if len(messages ) >=1:
            # Let the queue know that the message is processed
            g = git.cmd.Git(local_path)
            g.pull()
        for message in messages:
            message.delete()
        time.sleep(10)

if __name__ == '__main__':
        myname=os.path.basename(sys.argv[0])
        pidfile='/tmp/%s' % myname       # any name
        daemon = Daemonize(app=myname,pid=pidfile, action=main)
        daemon.start() 
