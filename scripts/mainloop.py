from lib.config import my_id
from threading import Thread
from requests import get, post
from time import sleep


def main():
	token = getToken()
	method = "messages.send"
	params = "user_id={}&message=Suka bliad".format(my_id)
	template = "https://api.vk.com/method/{}".format(method)
	args = {"user_id":my_id, "message":"Suka", "access_token":token}
	get(template, args)


def getToken():
	with open("token.txt") as f:
		return f.read().strip()


if __name__ == "__main__":
	# with ErrorManager("MultiThread bot"):
	main()

# def prnt():
# 	print(1)
# 	print(2)

# def wait():
# 	sleep(1)
# 	print(3)
# 	sleep(1)

# a = Thread(target=wait)
# b = Thread(target=prnt)

# a.start()
# b.start()
# print("starts finished")