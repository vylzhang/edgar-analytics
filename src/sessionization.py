import sys
import datetime

# sys args format below
#        0                       1               2                             3
# python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt

def get_inactivity_period():
	f = open(sys.argv[2], 'r')
	inactivity_period = int(f.read())
	return inactivity_period
	f.close()

def write_to_output(line):
	f = open(sys.argv[3], 'a')
	f.write(line + "\n")
	f.close()

def datetime_to_string(dt):
	return dt.strftime("%Y-%m-%d %H:%M:%S")

def string_to_datetime(str):
	return datetime.datetime.strptime(str, "%Y-%m-%d%H:%M:%S")

def user_session_data(user):
	time_elapsed = int( (user[2] - user[0]).total_seconds() + 1)
	start = datetime_to_string(user[0])
	end = datetime_to_string(user[2])
	count = str(user[1])
	return [start, end, str(time_elapsed), count]

def run():
	inactive = get_inactivity_period()
	fields = {"ip", "date", "time", "cik", "accession", "extention"}
	cols = {}

	f = open(sys.argv[1])
	header = f.readline().rstrip().split(',')
	# save the column position of the fields we care about
	for i in xrange(len(header)):
		if header[i] in fields:
			cols[header[i]] = i
	
	# users = {ip: [start_request_time, count, last_request_time]}
	# - upon encountering ip, update count and last_request_time
	# expiry_list = [ip] 
	# - at expiry time, remove matches (from this list and users dict) and write to output file
	users = {}
	expiry_list = [None] * inactive
	
	# read rest of input
	prev_time = 0
	for i, line in enumerate(f):
		data_line = line.rstrip().split(',')

		u_id = data_line[cols["ip"]]
		# lambda x: x[cols["date"]] + x[cols["time"]]
		string_date = data_line[cols["date"]]+data_line[cols["time"]]
		current_time = string_to_datetime(string_date)

		if u_id in users:
			users[u_id][1] += 1
			users[u_id][2] = current_time
			for e in expiry_list:
				if e and u_id in e:
					e.remove(u_id)
			expiry_list[-1].append(u_id)
		else:
			users[u_id] = [current_time, 1, current_time]
			expiry_list.append([u_id])

		# we are now at the next second, time to check expiry list
		if current_time != prev_time:
			ips_to_remove = expiry_list.pop(0)
			if ips_to_remove:
				for ip in ips_to_remove:
					write_to_output(','.join([ip] + user_session_data(users[ip])))
					users.pop(ip)
		
		prev_time = current_time

	# end of file, print remaining users
	for ip in sorted(users, key=users.get):
		write_to_output(','.join([ip] + user_session_data(users[ip])))

run()
