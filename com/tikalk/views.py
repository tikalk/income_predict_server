import os.path
import config
import uuid
import json

from flask import Blueprint, request, Response
from com.tikalk.predict.utils import predict, predict_income

log = config.configure_logging()
conf = config.get_config()


views = Blueprint('views', __name__)

users_data = {}


"""
age: continuous.
workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
fnlwgt: continuous.
education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
education-num: continuous.
marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
sex: Female, Male.
capital-gain: continuous.
capital-loss: continuous.
hours-per-week: continuous.
native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
"""
fields = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
          'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
          'hours-per-week', 'native-country']

all_fields = fields[:]
all_fields.append('income')

csv_file = '/Users/keren/tikalk/income_predict_server/data.csv'

def create_file(csv_file):
    with open(csv_file, 'a') as income_file:
        income_file.write(', '.join(all_fields))
        income_file.write('\n')


@views.route('/api/v1/predict', methods=['POST'])
def http_predict():
    log.debug('request ' + str(request.json))
    if not request.json or len(request.json) != 14:
        missing = [x for x in fields if x not in request.json]
        return Response('Missing attributes: {}'.format(', '.join(missing)),
                        status=400, mimetype='application/json')

    uid = uuid.uuid4()
    user_info = {
        'age': request.json['age'],
        'workclass': request.json['workclass'],
        'fnlwgt': request.json['fnlwgt'],
        'education': request.json['education'],
       'education_num': request.json['education-num'],
        'marital_status': request.json['marital-status'],
        'occupation': request.json['occupation'],
       'relationship': request.json['relationship'],
       'race': request.json['race'],
       'sex': request.json['sex'],
        'capital_gain': request.json['capital-gain'],
        'capital_loss': request.json['capital-loss'],
        'hours_per_week': request.json['hours-per-week'],
        'native_country': request.json['native-country'],
    }
    # collect data
    users_data[uid.hex] = user_info

    # call predict
    # income = predict('/Users/keren/tikalk/income_predict_server/tree-model.xml', user_info)
    income = predict_income(user_info)
    print 'income: {}'.format(income)
    return json.dumps({"id": uid.hex, "predict": income})

@views.route('/api/v1/income', methods=['POST'])
def http_income():
    log.debug('request ' + str(request.json))
    if request.json and 'id' in request.json and 'income' in request.json:
        user_info = users_data.pop(request.json['id'])
        user_info['income'] = '>=50K' if request.json['income'] >= 50000 else '<50K'
        if os.path.isfile(csv_file) is False:
            create_file(csv_file)

        # append to file
        with open(csv_file, 'a') as income_file:
            income_file.write(', '.join([str(user_info[x]) for x in all_fields]))
            income_file.write('\n')
        return "200"
