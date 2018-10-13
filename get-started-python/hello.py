from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
#import psycopg2
#conn = psycopg2.connect("host=d38168f5-328f-4274-b879-f62e803dbee8.8f7bfd8f3faa4218aec56e069eb46187.databases.appdomain.cloud dbname=marcello user=ibm_cloud_b05ee7ea_57e9_482c_ae10_056ed5d02f4d password=23602ed097ea5d85aaae5036cfb73b6d1692e8051914cd39794145ac0da29820")

app = Flask(__name__, static_url_path='')

db_name = 'marcello'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['databases-for-postgresql'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        print(creds)
        print(user)
        print(password)
        print(url)
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

def insert_faa(firstName,lastName, address, droneid):
    query = "INSERT INTO faa(firstName,lastName, address, droneid) " \
            "VALUES(%s,%s,%s,%s)"
    args = (firstName,lastName, address, droneid)

    try:
        db_config =
        conn =

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
