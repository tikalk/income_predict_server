from lxml import etree


def predict_income(values):
    if values['age'] > 30:
        if values['workclass'] in ['Private', 'Self-emp-not-inc', 'Self-emp-inc']:
            if values['education'] in ['Bachelors', 'Some-college']:
                if values['occupation'] in ['Sales', 'Exec-managerial', 'Prof-specialty']:
                    if values['hours_per_week'] > 40:
                        return True
    return False

def predict(model, values):
    tree = etree.parse(model)
    root = tree.getroot()

    # TODO: check values into DataDictionary
    if 'TreeModel' in [etree.QName(e).localname for e in root]:
        return predict_tree_model(model, values)

    raise Exception("Only TreeModel suported at this time. Be free to contribute!")


def predict_tree_model(model, values):
    predict = None

    tree = etree.parse(model)
    root = tree.getroot()
    tree_model = root.find('{http://www.dmg.org/PMML-4_3}TreeModel')

    # TODO: check values into MiningField

    Node = tree_model.find('{http://www.dmg.org/PMML-4_3}Node')
    predict = Node.get("score")
    pct = 0.5
    n_tot = Node.get("recordCount")
    n_predict = next(x.get('recordCount') for x in Node if
                     etree.QName(x).localname == 'ScoreDistribution' and x.get('value') == predict)
    count = 0
    while True:
        count +=1
        print count
        try:

            fill = next(e for e in Node
                        if etree.QName(e).localname == 'Node' and
                        unicode(values[e[0].get('field')]) == e[0].get('value'))

            try:
                Node = fill
                predict = Node.get("score")
                n_tot = Node.get("recordCount")
                n_predict = max(x.get('recordCount') for x in Node if
                                etree.QName(x).localname == 'ScoreDistribution' and x.get('value') == predict)
            except IndexError:
                break

            try:
                pct = float(n_predict) / float(n_tot)
            except:
                pct = 0.5
        except StopIteration:
            break

    return predict, pct
