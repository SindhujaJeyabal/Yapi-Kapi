from app import app
from libs import apis


def getlistFromApi():
	x=apis.get_master_data()
	