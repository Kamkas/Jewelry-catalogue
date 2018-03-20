from flask import Flask
from flask import render_template
from flask import jsonify, json

from models import Region

app = Flask(__name__)


@app.route('/regions', methods=['GET'])
def get_regions_list():
    r = Region()
    list = r.get_regions()
    return render_template('template.html', list=list)

@app.route('/region/<int:region_id>', methods=['GET'])
def get_region(region_id):
    r = Region()
    detail = r.get_region(kwargs={'id': region_id})
    return json.dumps(detail)

if __name__ == '__main__':
    app.run()
