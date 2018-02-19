from flask  import Flask, request, jsonify
from ast    import literal_eval

app = Flask(__name__)

@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
   content = request.json
   print content['SERVER_IP']
   print content['SERVER_PORT']
   print content['INIT_RAW']
   print content['ASSIGNED_NODE_NAME']
   print content['NODE_IP']
   print content['NODE_PORT']

   content['ASSIGNED_NODE_NAME'] = 'Node#1'
   content['INIT_RAW'] = 0     
   return jsonify(content)
   

if __name__ == '__main__':
   app.run(debug = True)
