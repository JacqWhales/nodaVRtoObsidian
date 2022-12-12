import csv
import re
import os

# Open the CSV file and read the data into a list of dictionaries,
# with the keys being the column names and the values being the
# corresponding cell values for each row.
with open('MetaverseNoda.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    rows = list(reader)

# Create an empty dictionary to store the Uuid to Title mapping.
uuid_to_title = {}

# Loop through each row in the data.
for row in rows:
    # Check if the row has a non-empty Uuid value.
    if row['Uuid']:
        # Add the Uuid and Title values to the dictionary.
        uuid_to_title[row['Uuid']] = row['Title']

for row in rows:
    # Check if the row has a non-empty FromUuid value.
    if row['FromUuid']:
        # Loop through the other rows in the data.
        for other_row in rows:
            # Check if the other row has a matching Uuid value in the FromUuid column.
            if other_row['Uuid'] == row['FromUuid']:
                # If a match is found, update the ToUuid value of the row
                # with the matching Uuid value to be the same as the
                # ToUuid value of the matching FromUuid row.
                if other_row['ToUuid']:
                    other_row['ToUuid'] = other_row['ToUuid'] + ', ' + row['ToUuid']
                else:
                    other_row['ToUuid'] = row['ToUuid']
                # Exit the inner loop once a matching Uuid value has been found.
                break

# Loop through the rows again.
for row in rows:
    # Check if the row has a non-empty ToUuid value.
    if row['ToUuid']:
        # Split the ToUuid value into a list of Uuid values.
        uuid_list = row['ToUuid'].split(',')

        # Loop through the Uuid values in the list.
        for uuid in uuid_list:
            # Remove leading and trailing whitespace from the Uuid value.
            uuid = uuid.strip()

            # Check if the Uuid value is in the dictionary.
            if uuid in uuid_to_title:
                # If the Uuid value is in the dictionary, use the re.sub()
                # function to replace all instances of the Uuid value
                # in the ToUuid string with the corresponding Title value.
                row['ToUuid'] = re.sub(uuid, uuid_to_title[uuid], row['ToUuid'])


# Create the output folder.
output_folder = 'output_files'
os.makedirs(output_folder, exist_ok=True)

# Loop through the rows again.
for row in rows:
    # Check if the row has an empty FromUuid value.
    if not row['FromUuid']:
        # Create the file name for the output file.
        filename = row['Title'] + '.md'
        # Join the output folder and file name to create the full path to the output file.
        filepath = os.path.join(output_folder, filename)

        # Open the output file for writing and write the data to the file.
        with open(filepath, 'w') as outfile:
            # Write the Title, FromUuid, and ToUuid values to the file.
            outfile.write(row['Title'] + '\n')
            # Split the ToUuid value on the comma, if it exists.
            to_uuids = row['ToUuid'].split(',')

            # Write each ToUuid value in double square brackets.
            outfile.write('[[{}]]'.format(to_uuids[0]))
            for uuid in to_uuids[1:]:
                outfile.write(' [[{}]]'.format(uuid))
            outfile.write('\n')
            
            # Write the additional data fields to the file.
            outfile.write('Uuid: {}\n'.format(row['Uuid']))
            outfile.write('Title: {}\n'.format(row['Title']))
            outfile.write('Notes: {}\n'.format(row['Notes']))
            outfile.write('ImageURL: {}\n'.format(row['ImageURL']))
            outfile.write('PageURL: {}\n'.format(row['PageURL']))
            outfile.write('Color: {}\n'.format(row['Color']))
            outfile.write('Opacity: {}\n'.format(row['Opacity']))
            outfile.write('Shape: {}\n'.format(row['Shape']))
            outfile.write('Size: {}\n'.format(row['Size']))
            outfile.write('PositionX: {}\n'.format(row['PositionX']))
            outfile.write('PositionY: {}\n'.format(row['PositionY']))
            outfile.write('PositionZ: {}\n'.format(row['PositionZ']))
            outfile.write('Collapsed: {}\n'.format(row['Collapsed']))
            outfile.write('Type: {}\n'.format(row['Type']))
            outfile.write('FromUuid: {}\n'.format(row['FromUuid']))
            outfile.write('ToUuid: {}\n'.format(row['ToUuid']))


