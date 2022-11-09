_CONTENT = {
	'pytest.ini': '''[pytest]
DJANGO_SETTINGS_MODULE = main.settings
python_files = tests.py test_*.py *_tests.py *_test.py
# feel free to replace `term` with `term:skip-covered`
addopts = --cov=. --cov-config=.coveragerc --cov-report term --cov-report html --cov-report xml
''',
	'.coveragerc': '''[run]
omit = */migrations/*, main/*, manage.py
'''
}
