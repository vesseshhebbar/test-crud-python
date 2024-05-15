from tinydb import TinyDB, Query
#from tinydb.storages import JSONStorage
#from tinydb.middlewares import CachingMiddleware
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Database setup
#db = TinyDB('db/tasks.json', storage=CachingMiddleware(JSONStorage))
db = TinyDB('db/tasks.json')
Task = Query()

def create_task(title, description, sub_tasks, attachments, due_date, priority, tags, person, location, recur_interval):
    task = {
        'title': title,
        'description': description,
        'sub_tasks': sub_tasks,
        'attachments': attachments,
        'due_date': due_date.isoformat() if isinstance(due_date, datetime) else due_date,
        'timestamp': datetime.now().isoformat(),
        'priority': priority,
        'tags': tags,
        'person': person,
        'location': location,
        'recur_interval': recur_interval
    }
    task_id = db.insert(task)
    return task_id

def read_task(task_id):
    return db.get(doc_id=task_id)

def update_task(task_id, updates):
    db.update(updates, doc_ids=[task_id])

def delete_task(task_id):
    db.remove(doc_ids=[task_id])

def list_tasks():
    return db.all()

def recur_task(task_id):
    task = read_task(task_id)
    if task and task['recur_interval']:
        recur_interval = task['recur_interval']
        next_due_date = datetime.fromisoformat(task['due_date']) + relativedelta(**recur_interval)
        new_task_id = create_task(
            task['title'], task['description'], task['sub_tasks'], task['attachments'],
            next_due_date, task['priority'], task['tags'], task['person'], task['location'], task['recur_interval']
        )
        return new_task_id
    return None
