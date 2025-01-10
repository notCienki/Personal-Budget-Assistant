import json

categories_path = "src/data/categories.json"
finance_path = "src/data/finance.json"

categories_file = open(categories_path, "r+")

categories_data = json.load(categories_file)

def get_categories():
    return categories_data['categories']

def add_category(name):
    id = 0
    for category in categories_data['categories']:
        if category['id'] > id:
            id = category['id']
    id += 1
    categories_data['categories'].append({'id': id, 'name': name})
    categories_file.seek(0)
    json.dump(categories_data, categories_file)
    categories_file.truncate()

def remove_category_by_name(name):
    for category in categories_data['categories']:
        if category['name'] == name:
            categories_data['categories'].remove(category)
            categories_file.seek(0)
            json.dump(categories_data, categories_file)
            categories_file.truncate()


def remove_category_by_id(id):
    for category in categories_data['categories']:
        if category['id'] == id:
            categories_data['categories'].remove(category)
            categories_file.seek(0)
            json.dump(categories_data, categories_file)
            categories_file.truncate()

def update_category_by_name(old_name, new_name):
    for category in categories_data['categories']:
        if category['name'] == old_name:
            category['name'] = new_name
            categories_file.seek(0)
            json.dump(categories_data, categories_file)
            categories_file.truncate()


