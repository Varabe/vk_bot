from lib.utils import vk


def findDogs(group_id):
	offset = 0
	dogs = []
	member_count = getGroupMembers(group_id, offset)['count']
	while offset != member_count:
		members = getGroupMembers(group_id, offset)['items']
		offset += len(members)
		accounts = getUserAccounts(members)
		dogs += getDogsFromAccounts(accounts)
	return dogs


def removeDogs(group_id):
	dogs = findDogs(group_id)
	for dog in dogs:
		removeDog(group_id, dog)
	if findDogs(group_id):
		removeDogs(group_id)


def removeDog(group_id, dog):
	vk("groups.removeUser", group_id=group_id, user_id=dog['id'])


def getGroupMembers(group_id, offset):
	max_amount = 1000
	return vk("groups.getMembers", group_id=group_id, offset=offset, count=max_amount)


def getUserAccounts(user_ids):
	return vk("users.get", user_ids=user_ids)


def getDogsFromAccounts(accounts):
	return [a for a in accounts if "deactivated" in a]
