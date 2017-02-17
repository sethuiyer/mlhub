''' 
Indexes result_struct.json in the elastic search server
'''
import elasticsearch
import json
es = elasticsearch.Elasticsearch()  
with open("result_struct.json") as f:
    data = json.load(f)
num_rec = len(data['imgblobs'])
new_d = [ {} for _ in xrange(num_rec)]

for _ in xrange(num_rec):
    new_d[_]['imgurl'] = data['imgblobs'][_]['img_path']
    new_d[_]['description'] = data['imgblobs'][_]['candidate']['text']
for i in xrange(num_rec):
    es.index(index="desearch", doc_type="json", id=i, body = {
                    'imgurl': new_d[i]['imgurl'],
                    'description': new_d[i]['description'],
                    'idnum': i
                })
