import time
import commands


def removeDogs(group_id, init=None):
	initial_count = count = api.groups.getMembers(group_id=group_id, count=0)['count']
	if init:
		initial_count = init
	offset = 0
	while offset != count:
		users = api.groups.getMembers(group_id=group_id, offset=offset)
		count = users['count']
		offset += len(users['items'])
		users = api.users.get(user_ids=users['items'])
		for user in users:
			if 'deactivated' in user:
				api.groups.removeUser(group_id=group_id, user_id=user['id'])
				offset -= 1
				time.sleep(sleepTime)
		time.sleep(sleepTime)
	if searchDogs(group_id):
		initial_count, count = removeDogs(group_id, initial_count)
	return initial_count, count


def searchDogs(group_id):
	offset = dogs = 0
	count = 1
	while count != offset:
		time.sleep(sleepTime)
		users = api.groups.getMembers(group_id=group_id, offset=offset)
		count = users['count']
		offset += len(users['items'])
		users = api.users.get(user_ids=users['items'])
		for user in users:
			if 'deactivated' in user:
				dogs += 1
		print("Count:{}, Dogs:{}".format(offset, dogs))
	percent = round((dogs/count) * 100)
	return count, dogs
