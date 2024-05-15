import argparse
from database import create_task, read_task, update_task, delete_task, list_tasks, recur_task
from datetime import datetime

import pprint

def parse_args():
    parser = argparse.ArgumentParser(description='Task Management CLI')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('--title', required=True)
    create_parser.add_argument('--description', required=True)
    create_parser.add_argument('--sub_tasks', nargs='*', default=[])
    create_parser.add_argument('--attachments', nargs='*', default=[])
    create_parser.add_argument('--due_date', required=True)
    create_parser.add_argument('--priority', type=int, required=True)
    create_parser.add_argument('--tags', nargs='*', default=[])
    create_parser.add_argument('--person', required=True)
    create_parser.add_argument('--location', required=True)
    create_parser.add_argument('--recur_interval', nargs='*', default=[])

    read_parser = subparsers.add_parser('read')
    read_parser.add_argument('--task_id', type=int, required=True)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('--task_id', type=int, required=True)
    update_parser.add_argument('--title')
    update_parser.add_argument('--description')
    update_parser.add_argument('--sub_tasks', nargs='*')
    update_parser.add_argument('--attachments', nargs='*')
    update_parser.add_argument('--due_date')
    update_parser.add_argument('--priority', type=int)
    update_parser.add_argument('--tags', nargs='*')
    update_parser.add_argument('--person')
    update_parser.add_argument('--location')
    update_parser.add_argument('--recur_interval', nargs='*')

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('--task_id', type=int, required=True)

    list_parser = subparsers.add_parser('list')

    recur_parser = subparsers.add_parser('recur')
    recur_parser.add_argument('--task_id', type=int, required=True)

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'create':
        due_date = datetime.fromisoformat(args.due_date)
        recur_interval = {args.recur_interval[i]: int(args.recur_interval[i+1]) for i in range(0, len(args.recur_interval), 2)}
        task_id = create_task(
            title=args.title,
            description=args.description,
            sub_tasks=args.sub_tasks,
            attachments=args.attachments,
            due_date=due_date,
            priority=args.priority,
            tags=args.tags,
            person=args.person,
            location=args.location,
            recur_interval=recur_interval
        )
        print(f'Task created with ID: {task_id}')
    elif args.command == 'read':
        task = read_task(args.task_id)
        pprint.pp(task)
    elif args.command == 'update':
        updates = {k: v for k, v in vars(args).items() if k not in ['command', 'task_id'] and v is not None}
        update_task(args.task_id, updates)
        print(f'Task {args.task_id} updated.')
    elif args.command == 'delete':
        delete_task(args.task_id)
        print(f'Task {args.task_id} deleted.')
    elif args.command == 'list':
        tasks = list_tasks()
        for task in tasks:
            print(task)
    elif args.command == 'recur':
        new_task_id = recur_task(args.task_id)
        if new_task_id:
            print(f'New recurring task created with ID: {new_task_id}')
        else:
            print('Task does not have a recurrence interval or could not be found.')

if __name__ == '__main__':
    main()
