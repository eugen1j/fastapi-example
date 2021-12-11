dev-deps:
	pip install --upgrade pip poetry
	poetry install

deps:
	pip install --upgrade pip poetry
	poetry install --no-dev

#server:
#	python manage.py migrate && python manage.py init_rbac && python manage.py runserver
#
#queue:
#	python manage.py rundramatiq

lint:
	#make lint-commits
	flake8 app
	mypy app

clean-lint:
	#make lint-commits
	isort .
	autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports app
	black app
	flake8 app
	mypy app

#test:
#	pytest -n 4 -x
#
install-hooks:
	# We use a '#' symbol in the start of the commit msg title
	# to mention a Gitlab issue. So we should change commentChar to ';'
	git config core.commentChar ";"
	cp ./git/hooks/pre-commit .git/hooks/
	cp ./git/hooks/commit-msg .git/hooks/

lint-commits:
	# We use a '#' symbol in the start of the commit msg title
	# to mention a Github issue. So we should change commentChar to ';'
	git config core.commentChar ";"
	# Check last commit message
	gitlint
