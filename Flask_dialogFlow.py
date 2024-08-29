import json
import psycopg2
from flask import Flask, request, jsonify
#pip install autopep8 allows for formatting of the code
#initialize the Flask app
app = Flask(__name__)



@app.route('/dialogflow', methods=['GET', 'POST'])
def dialogflow():

    data = request.get_json()
    print(json.dumps(data))

    return jsonify(
        {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': ['This is a sample response from webhook.']
                        }
                    }
                ]
            }
        }
    )




#run the app
if __name__ == '__main__':
    #app.run()
    app.run(debug=True)