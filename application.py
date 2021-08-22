from flask import Flask,request,Response
from flask import render_template,redirect,url_for,flash
import io,os,json
import csv
import boto3,botocore
import pandas as pd
import itertools
import numpy as np
from boto3.dynamodb.conditions import Key, Attr


application = Flask(__name__)
application._static_folder = './static/'
application.config['SESSION_TYPE'] = 'filesystem'
application.secret_key = "Ishanth7#"

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id="###",
    aws_secret_access_key="###",
    region_name="us-east-2"
)

table = dynamodb.Table('SourceData')

@application.route("/")
def index():
    return render_template('login.html')

@application.route("/home")
def home():
    return render_template('index.html')

@application.route("/logout")
def logout():
    return redirect(url_for('index'))

@application.route("/register")
def register():
    return render_template('signup.html')


@application.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        if response['Items']:
            flash("User already exists. Please login","info")
            return redirect(url_for('index'))

        try:
            table.put_item(
                    Item={
            'email': email,
            'password': password
                }
            )
        except Exception as e:
            flash("Server error. Please try again","danger")
            return redirect(url_for('register'))

        flash("Registration successful. Please login to continue","success")
        return redirect(url_for('index'))

    flash("Invalid method request","danger")
    return redirect(url_for('register'))

@application.route('/login',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        items = response['Items'][0]

        if items:
            email,orig_password = items["email"],items["password"]
            if str(password) == orig_password:
                return redirect(url_for('home'))
        
        flash("Invalid email or password","danger")
        return redirect(url_for('index'))
    
    flash("Invalid method request","danger")
    return redirect(url_for('index'))
    
@application.route("/download",methods=['POST'])
def download():
    f = request.files['downloadfile']
    if not f:
        flash('Please upload a file','danger')
        return redirect(url_for('home'))

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    zips = list(itertools.chain(*csv_input))

    output = []
    for zipCode in zips[1:]:
        response = table.get_item(
                    Key={
                    'Zip': str(int(zipCode)),
                    })
        if "Item" in response:
            item = response['Item']
            output.append(dict(item))
        else:
            item = dict({'Zip':zipCode})
            output.append(item)
        
    df = pd.DataFrame(output)

    return Response(
        df.to_csv(na_rep='N/A',index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=FilteredData.csv"})

@application.route("/upload",methods=['POST'])
def upload():
    f = request.files['uploadfile']
    if not f:
        flash('Please upload a file','danger')
        return redirect(url_for('home'))

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    total_data = list(csv_input)
    data,columns = total_data[1:],total_data[0]
    df = pd.DataFrame(data,columns=columns)
    df = df.replace('N/A',np.NaN)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    if df.isnull().values.any(): 
        
        flash('Null values found. Please verify','danger')
        return redirect(url_for('home'))

    dtypes = ['str','str','datetime64','str','str']
    
    for column,dataType in zip(columns,dtypes):
        try:
            df[column] = df[column].astype(dataType)
        except Exception as e:
            flash('Bad values found in {} column. They should be of {} datatype'.format(column,dataType),'danger')
            return redirect(url_for('home'))

    for row in df.itertuples(index=True):
        zipCode = df.iloc[row.Index]['Zip']
        response = table.get_item(
                    Key={
                    'Zip': str(int(zipCode)),
                    })
        
        if "Item" not in response:
            try:
                item = json.loads(df.iloc[row.Index].to_json(date_format='iso')) 

                table.put_item(
                        Item = {
                            'Zip':item['Zip'],
                            'Product':item['Product'],
                            'ORG User':item['ORG User'],
                            'Modified User':item['Modified User'],
                            'Recorded':str(item['Recorded'])[:10]
                        } )


            except Exception as e:
                print(e)
    
    flash('Records updated succesfully','success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    application.run(host='127.0.0.1',port=8000,debug=True)