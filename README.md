# Approach

My approach uses two main data structures:
1. a map of users that maps ip to (start_request_time, doc_count, last_request_time)
2. a queue of expiring ips, with length of the given inactivity period

As the requests are being read, each new ip address is added to the map of users.
If the user has been seen before, simply update their entry in the map to reflect the new doc_count and last_request_time.
To keep the expiring ip list fresh, add ip addresses to the end of the queue and make sure any previous entry is removed.

Since the expiring ip list was initialized to be the same length as the inactivity period, when the time progresses one second, we know that we can now look at the beginning of our expiring ip list to find all the expiring ips at this time. Simply dequeue them, get the session info from the corresponding user map entries, and remove the ip from both the expiring list and the user map.

Finally, once the end of the file has been reached, output all the remaining users in the map regardless of inactivity period.
