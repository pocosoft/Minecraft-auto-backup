import os
import shutil
import datetime
import json
from time import sleep

HOME_DIR = os.path.expanduser('~')
MINECRAFT_PATH = os.path.join(HOME_DIR, 'Library', 'Application Support', 'minecraft')
SAVED_DIR = os.path.join(MINECRAFT_PATH, 'saves')
BACKUP_DIR = os.path.join(MINECRAFT_PATH, 'backups')
LAST_SIZE_PATH = os.path.join(BACKUP_DIR, 'auto_backup_size.json')

if not os.path.exists(LAST_SIZE_PATH):
    with open(LAST_SIZE_PATH, 'w') as f:
        f.write('{}')


def target_fullpath() -> [str]:
    dir_list = os.listdir(SAVED_DIR)
    dir_list.remove('.DS_Store')
    full_path = []
    for d in dir_list:
        full_path.append(os.path.join(SAVED_DIR, d))
    return full_path


def get_size_dir(path: str) -> int:
    total_size = 0
    for dir_path in os.listdir(path):
        full_path = os.path.join(path, dir_path)
        if os.path.isfile(full_path):
            total_size += os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            total_size += get_size_dir(full_path)
    return total_size


def is_changed(path: str) -> bool:
    with open(LAST_SIZE_PATH) as f:
        sizes = json.load(f)
    last_size = sizes.get(path)
    current_size = get_size_dir(path)
    sizes[path] = current_size
    print(sizes)
    with open(LAST_SIZE_PATH, mode='w') as f:
        json.dump(sizes, f)
    return current_size != last_size


def backup():
    targets = target_fullpath()
    for target in targets:
        target_name = os.path.basename(target)
        print('{} Backup start.'.format(target_name))
        if is_changed(target):
            now = datetime.datetime.now()
            cp_to = os.path.join(BACKUP_DIR, '{}_{}_auto_backup'.format(now.strftime('%Y%m%d%H%M%S'), target_name))
            shutil.make_archive(cp_to, 'zip', root_dir=target)
            print('{} Backup success.'.format(target_name))
        else:
            print('{} Backup pended.'.format(target_name))


if __name__ == '__main__':
    backup()
    while True:
        sleep(600)
        backup()

