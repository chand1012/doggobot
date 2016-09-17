from json import dumps
# this will create a file for the times to post photos
times = []
while True:
    a_time = [raw_input('Enter time to post at: ')]
    if a_time == '':
        break
    else:
        times += a_time

counter = 1
data = {}
for a_time in times:
    data['time{}'.format(counter)] = a_time
    counter += 1

json_data = dumps(data)
json_file = open('times.json', 'w+')
json_file.write(json_data)
json_file.close()

print "File successfully written."
