from flask import Flask,request,Response
from flask import render_template,redirect,url_for,flash
import io,os,json
import csv
import boto3,botocore
import pandas as pd
import itertools
import numpy as np

application = Flask(__name__)
application._static_folder = './static/'
application.config['SESSION_TYPE'] = 'filesystem'
application.secret_key = "Ishanth7#"

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id="##",
    aws_secret_access_key="##",
    region_name="us-east-2"
)

table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')