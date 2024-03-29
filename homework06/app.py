import json
import datetime
import redis
import petname
import uuid
import random
from flask import Flask, request

rd=redis.StrictRedis(host='10.99.252.240', port=6379, db=0)

app= Flask(__name__)

def getdata():
	userdata=json.loads(rd.get('animals').decode('utf-8'))
	return userdata

@app.route('/animals/reset/', methods=['GET'])
def animals_reset():
    animal_dict = {}
    animal_dict['animals'] = []

    for i in range(20):
        this_animal = {}
        this_animal['head'] = random.choice(['snake', 'bull', 'lion', 'raven', 'bunny'])
        this_animal['body'] = petname.name() + '-' + petname.name()
        this_animal['arms'] = random.randint(1,5) * 2
        this_animal['legs'] = random.randint(1,4) * 3
        this_animal['tail'] = this_animal['legs'] + this_animal['arms']
        this_animal['created_on'] = str(datetime.datetime.now())
        this_animal['uuid'] =str(uuid.uuid4())

        animal_dict['animals'].append(this_animal)

    rd.set('animals', json.dumps(animal_dict, indent=2))
    return str('success')

@app.route('/animals', methods=['GET'])
def get_animals():

	return json.dumps(getdata(),indent=2)

@app.route('/animals/daterange/',methods=['GET'])
def animals_in_daterange():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	animalsDates=[]
	beg=request.args.get('beginning_date')
	end=request.args.get('end_date')
	
	beg_date=datetime.datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
	end_date=datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')

	for x in animalsList:
		if(x['created_on']>beg_date and x['created_on']<end_date):
			animalsDates.append(x)
	return json.dumps(animalsDates, indent=2)


@app.route('/animals/uuid_select/', methods=['GET'])
def animals_uuid_select():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	uuid=request.args.get('uuid')
	for x in animalsList:
		if (x['uuid']==uuid):
			return x


@app.route('/animals/uuid_edit/',methods=['GET'])
def animals_uuid_edit():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	uuid=request.args.get('uuid')
	for x in animalsList:
		if(x['uuid']==uuid):
			arms=x['arms']
			x['arms']=arms+1
			break
	rd.set('animals',json.dumps(animalsList, indent=2))
	return json.dumps(animalsList, indent=2)
	 

@app.route('/animals/delete_daterange/', methods=['GET'])
def animals_delete_daterange():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	delete=[]
	beg=request.args.get('beginning_date')
	end=request.args.get('end_date')
	
	beg_date=datetime.datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
	end_date=datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
	for x in animalsList:
		if (x['created_on']>beg_date and x['created_on']<end_date):
			animalsList.remove(x)

	rd.set('animals', json.dumps(animalsList, indent=2))
	return json.dumps(animalsList, indent=2)
	
@app.route('/animals/avg_legs/', methods=['GET'])
def animals_avg_legs():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	total_legs=0
	for x in animalsList:
		total_legs+=x['legs']
	avg_legs=total_legs/len(animalsList)
	return str(avg_legs)

@app.route('/animals/total/',methods=['GET'])
def animals_total():
	animal_dict=getdata()
	animalsList=animal_dict['animals']
	total=len(animalsList)

	return str(total)

		
if __name__=='__main__':

	app.run(debug=True, host='0.0.0.0')
