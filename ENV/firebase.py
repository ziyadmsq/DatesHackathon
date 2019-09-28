import firebase_admin
import time
import random
import math
from random import randrange
from firebase_admin import credentials, auth, firestore
from datetime import datetime, timedelta, date

cred = credentials.Certificate('dates-health-service-account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
transaction = db.transaction()


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_random_name(letters):
    email_name = ""
    for i in range(10):
        email_name += letters[random.randint(0, 25)]

    return email_name


def get_random_email():
    domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com" , "yahoo.com"]
    letters = [chr(ord('a')+i) for i in range(26)]

    name = get_random_name(letters)
    domain = random.choice(domains)

    return name, name + '@' + domain


def generate_owners(num):
    for i in range(num):
        print(f'[INFO] Generating Owner: ({i+1}/{num})')
        name, email = get_random_email()

        user = auth.create_user(
            email=email,
            email_verified=False,
            password='123abc',
            display_name=name,
            disabled=False
        )

        generate_data(user.uid)
        user_ref = db.collection(u'users').document(user.uid).set({
            u'isOwner': True
        })


def generate_data(owner):
    workers = generate_workers(owner)
    generate_farm(owner, workers)


def generate_farm(owner, workers):
    num = random.randint(60, 100)
    trees = []

    for i in range(num):
        print(f'[INFO] Generating Tree: ({i+1}/{num})')
        tree = generate_tree()
        tree['owner'] = owner
        tree['worker'] = random.choice(workers)

        tree_ref = db.collection(u'trees').document().set(tree)



def generate_tree():
    format = '%m/%d/%y %H:%M:%S'
    date_start = datetime.strptime('09/24/17 13:55:26', format)
    date_end = datetime.strptime('09/26/19 13:55:26', format)
    types = ["Barhi", "Thoory", "Halawi", "Medjool", "Khadrawy", "Deglet Noor", "Fard", "Zahidi", "Dayri"]

    tree = {}

    age = random.randint(20, 150)
    type = random.choice(types)
    harvest_list = []
    water_list = []
    pesticide_list = []
    temp_list = []

    tree['age'] = age
    tree['type'] = type
    tree['harvest'] = harvest_list
    tree['water'] = water_list
    tree['pesticide'] = pesticide_list
    tree['temp'] = temp_list

    for i in range(random.randint(100, 200)):
        date = random_date(date_start, date_end)
        harvest_amount = random.randint(20, 150)
        harvest_quality = random.choice(['LOW', 'MID', 'HIGH'])

        water_amount = random.randint(20, 80)

        pesticide_amount = random.randint(10, 100)

        temp_degree = random.randint(15, 40)
        temp_soil_humidity = random.randint(10, 100)
        temp_air_humidity = random.randint(10, 100)

        harvest_list.append({
            'date': date,
            'amount': harvest_amount,
            'quality': harvest_quality
        })

        water_list.append({
            'date': date,
            'amount': water_amount
        })

        pesticide_list.append({
            'date': date,
            'amount': pesticide_amount
        })

        temp_list.append({
            'date': date,
            'degree': temp_degree,
            'soil_humidity': temp_soil_humidity,
            'air_humidity': temp_air_humidity
        })

    return tree


def generate_workers(owner):
    format = '%m/%d/%y %H:%M:%S'
    date_start = datetime.strptime('01/19/19 13:55:26', format)
    date_end = datetime.strptime('09/26/19 13:55:26', format)

    workers = []
    num_w = random.randint(3, 10)

    for i in range(num_w):
        print(f'[INFO] Generating Worker: ({i+1}/{num_w})')
        name, email = get_random_email()
        num = random.randint(3, 10)

        user = auth.create_user(
            email=email,
            email_verified=False,
            password='123abc',
            display_name=name,
            disabled=False
        )

        date = random_date(date_start, date_end)

        data = {
            u'owner': owner,
            u'latestSubmission': date,
            u'isOwner': False
        }

        user_ref = db.collection(u'users').document(user.uid).set(data)
        workers.append(user.uid)

    return workers


def post_health_report(data):
    tree_ref = db.collection(u'trees').document(data['id'])

    data_doc = {
        'date': datetime.now(),
        'degree': data['degree'],
        'soil_humidity': data['soil_humidity'],
        'air_humidity': data['air_humidity']
    }

    update_in_transaction(transaction, tree_ref, data_doc)


@firestore.transactional
def update_in_transaction(transaction, tree_ref, data):
    snapshot = tree_ref.get(transaction=transaction)
    temp = snapshot.get(u'temp')

    temp.append(data)

    transaction.update(tree_ref, {
        u'temp': temp
    })


def get_trees(owner):
    tree_docs = db.collection(u'trees').where(u'owner', u'==', owner).stream()
    tree_ids = []

    for doc in tree_docs:
        tree_ids.append(doc.id)

    return tree_ids


def get_tree(id):
    tree_doc = db.collection(u'trees').document(id).get()
    return tree_doc.to_dict()


def get_workers(owner):
    worker_docs = db.collection(u'users').where(u'owner', u'==', owner).stream()
    worker_ids = []

    for doc in worker_docs:
        worker_ids.append(doc.id)

    return worker_ids


def get_worker(id):
    worker_doc = db.collection(u'users').document(id).get()
    trees = get_worker_trees(id)
    worker_dict = worker_doc.to_dict()
    worker_dict['trees'] = trees
    return worker_dict


def get_worker_trees(worker):
    tree_docs = db.collection(u'trees').where(u'worker', u'==', worker).stream()
    tree_ids = []

    for doc in tree_docs:
        tree_ids.append(doc.id)

    return tree_ids


def get_recent(owner):
    tree_docs = db.collection(u'trees').where(u'owner', u'==', owner).stream()
    harvest_count = [0 for i in range(24)]
    water_count = [0, 0]
    pesticide_count = [0, 0]

    for doc in tree_docs:
        tree_dict = doc.to_dict()
        water_list = tree_dict['water']
        harvest_list = tree_dict['harvest']
        pest_list = tree_dict['pesticide']

        today = date.today()

        for water in water_list:
            for i in range(1, 3):
                d = (today - timedelta(days=30*i))
                datex = datetime(d.year, d.month, d.day)
                if water['date'] > datex:
                    water_count[i-1] += water['amount']
                    break

        for pest in pest_list:
            for i in range(1, 3):
                d = (today - timedelta(days=30*i))
                datex = datetime(d.year, d.month, d.day)
                if pest['date'] > datex:
                    pesticide_count[i-1] += pest['amount']
                    break

        for harvest in harvest_list:
            for i in range(1, 25):
                d = (today - timedelta(days=30*i))
                datex = datetime(d.year, d.month, d.day)
                if harvest['date'] > datex:
                    harvest_count[i-1] += harvest['amount']
                    break

    data = {
        'water': water_count,
        'pesticide': pesticide_count,
        'harvest': harvest_count
    }

    return data

if __name__ == '__main__':
    generate_owners(1)
