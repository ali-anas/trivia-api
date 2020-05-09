import os
SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

db_details = {
	"prod_db_name": "trivia",
	"test_db_name": "trivia_test",
	"user": "tester",
	"password": "pass123"
}