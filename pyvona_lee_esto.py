# -*- coding: utf-8 -*-
import boto3
import os
import sys

polly_client = boto3.Session(
    aws_access_key_id= '',                     
    aws_secret_access_key='',
    region_name='us-west-2').client('polly')


f = open('test.txt', 'r')

response = polly_client.synthesize_speech(
	VoiceId='Mia',
    OutputFormat='mp3', 
    Text = f.read())

file = open('respuesta.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()
os.system("mpg123 -q respuesta.mp3")