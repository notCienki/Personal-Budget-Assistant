import json

categories_path = "src/data/categories.json"

# Load categories data
categories_file = open(categories_path, "r+")
categories_data = json.load(categories_file)

def get_all_categories():
    """
    Get all categories
    """
    return categories_data['categories']

def get_category_by_id(id):
    """
    Get category by ID
    """
    categories = categories_data['categories']
    for category in categories:
        if category['id'] == id:
            return category
    return None

def get_category_by_name(name):
    categories = categories_data['categories']
    for category in categories:
        if category['name'] == name:
            return category
    return None

def add_category(name):
    """
    Add new category
    """
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
    """
    Remove category by name
    """
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
    """
    Update category name
    """
    for category in categories_data['categories']:
        if category['name'] == old_name:
            category['name'] = new_name
            categories_file.seek(0)
            json.dump(categories_data, categories_file)
            categories_file.truncate()


