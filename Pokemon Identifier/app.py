from poketype import PokemonTypeIdentifier
from flask import Flask, request, make_response,jsonify
import os
id = PokemonTypeIdentifier()
app = Flask(__name__,static_url_path='/static')

@app.route('/findtype',methods=['GET'])
def classify():
    poke_name=request.args.get('pokename')
    results = id.predict_type(poke_name)
    return jsonify({'results':results})
@app.route('/',methods=['GET'])
def root():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(debug=True,host='0.0.0.0',port=port,use_reloader=False)
