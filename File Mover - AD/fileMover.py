import csv, os, shutil

csv_filename = 'Imported table-Jan2020 copy 2.csv'
dry_run = False
number_to_process = 100
name_to_folder_dict = {}
file_ext_to_ignore = ['csv', 'py']
filesmoved = 0

with open(csv_filename, 'r', encoding='utf-8-sig') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        name_to_folder_dict[row['Name'].split('.')[0]] = row['Release Season']
        name_to_folder_dict[row['Maximum of Group Image Name']] = row['Release Season']


with os.scandir() as entries:
    files = [entry.name for entry in entries if (entry.is_file() and (entry.name)[0] != '.' and (entry.name).rsplit('.',1)[1] not in file_ext_to_ignore)]
    print(str(len(files)) + ' files present')

for filename in files:
    root_filename = (filename.rsplit('.',1)[0]).split('-')[0]
    if root_filename not in name_to_folder_dict:
        print(filename + ' with root filename [' + root_filename + '] not found')
        continue

    destination_folder = name_to_folder_dict[root_filename]
    destination_path = os.path.join(destination_folder, filename)

    if not dry_run:
        os.makedirs(destination_folder, exist_ok=True)
        shutil.move(filename, destination_path)
        filesmoved+=1
    print('Move ['+ filename + '] to ' + destination_path)

    number_to_process-=1

    if number_to_process == 0:
        break

print('Files moved:' + str(filesmoved))