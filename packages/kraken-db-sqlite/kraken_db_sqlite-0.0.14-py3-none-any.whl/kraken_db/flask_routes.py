
import os
from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify

import kraken_db.kraken_db as db
import kraken_db.kraken_data_proc as proc





# Initalize app
test_mode = False


# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['GET'])
def main_get():
    """Process get data
    """

    content = '''
    Database server.
    Access through /api
    /api
        - get: 
            - args: record_type, record_id, key, value
            - return: list of observations
        - post: 
            - args: json list of observation records
            - return: ok
    /api/summary
        - get: 
            - args: record_type, record_id, key, value
            - return: max observation for each key
    
    /search
        - post: 
            - args: 
                -'key_name' = 'value' - list of things to search
                - limit:
                - offset:
                - order_by
                - order_direction
            - return:
                - list of observations
    
    '''

    return Response(content)

@app.route('/api', methods=['GET'])
def api_get():
    """Process get data
    """


    record_type = request.values.get('record_type', None)
    record_id = request.values.get('record_id', None)
    key = request.values.get('key', None)
    value = request.values.get('value', None)

    records = db.get(record_type, record_id, key, value)

    return jsonify(records)



@app.route('/api', methods=['POST'])
def api_post():
    """Process get data
    """
    
    record = request.get_json()
  
    print('record', record)
    if not record:
        return Response('none')


    db.post(record)
    
    return Response('ok')





@app.route('/api/schemas', methods=['GET'])
def api_schemas():
    """Return schemas and count
    """

    records = db.list_record_types()

    return jsonify(records)



@app.route('/api/summary', methods=['GET'])
def api_summary():
    """Process get data
    """
    
    order_by = None
    order_direction = None
    limit = None
    offset = None
    format = None

    params = []
    for i in request.values:
        if i == 'limit':
            limit = request.values.get(i, None)
        elif i == 'offset':
            offset = request.values.get(i, None)
        elif i == 'order_by':
            order_by = request.values.get(i, None)
        elif i == 'order_direction':
            order_direction = request.values.get(i, None)
        elif i == 'format':
            format = request.values.get(i, None)        
        else:
            param = (i, '==', request.values.get(i, None))
            params.append(param)

    records = db.search(params, order_by, order_direction, limit, offset)

    # Transform to records if json
    if format == 'json':
        records = proc.obs_to_dict(records)
    
    
    return jsonify(records)

@app.route('/api/search', methods=['GET'])
def api_search():
    """Process get data
    """
    
    order_by = None
    order_direction = None
    limit = None
    offset = None
    response_format = None

    params = []
    for i in request.values:
        if i == 'limit':
            limit = request.values.get(i, None)
        elif i == 'offset':
            offset = request.values.get(i, None)
        elif i == 'order_by':
            order_by = request.values.get(i, None)
        elif i == 'order_direction':
            order_direction = request.values.get(i, None)
        elif i == 'format':
            response_format = request.values.get(i, None)        
        else:
            param = (i, '==', request.values.get(i, None))
            params.append(param)

    records = db.search(params, order_by, order_direction, limit, offset)

    # Transform to records if json
    if response_format == 'json':
        records = proc.obs_to_dict(records)
    
    
    return jsonify(records)


def run_api():
    app.run(host='0.0.0.0', debug=False)

