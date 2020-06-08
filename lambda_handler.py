import json
import os
import sys
import boto3
import uuid
import datetime
s3_client=boto3.client('s3')

from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def convert_transcript(infile,outfile):
    print ("Filename: ", infile)
    with open(outfile,'w+') as w:
        data=infile
        labels = data['results']['speaker_labels']['segments']
        speaker_start_times={}
        for label in labels:
                for item in label['items']:
                        speaker_start_times[item['start_time']] =item['speaker_label']
        items = data['results']['items']
        lines=[]
        line=''
        time=0
        speaker='null'
        i=0
        for item in items:
                i=i+1
                content = item['alternatives'][0]['content']
                if item.get('start_time'):
                        current_speaker=speaker_start_times[item['start_time']]
                elif item['type'] == 'punctuation':
                        line = line+content
                if current_speaker != speaker:
                        if speaker:
                                lines.append({'speaker':speaker, 'line':line, 'time':time})
                        line=content
                        speaker=current_speaker
                        time=item['start_time']
                elif item['type'] != 'punctuation':
                        line = line + ' ' + content
        lines.append({'speaker':speaker, 'line':line,'time':time})
        sorted_lines = sorted(lines,key=lambda k: float(k['time']))
        for line_data in sorted_lines:
                line='[' + str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get('speaker') + ': ' + line_data.get('line')
                w.write(line + '\n\n')

def lambda_handler(event, context):
    convert_transcript(event,'/tmp/output.txt')
    upload_file('/tmp/output.txt', 'pdap-transcribe', object_name='transcript.txt')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        # 'body': json.dumps(str(event)),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }

    }
