package-publish:
	rm -rf ./dist
	python setup.py sdist
	twine upload dist/*

coverage:
	pytest --cov=wc_shortcodes --cov-report html tests/

test:
	ptw --runner="pytest --cov=wc_shortcodes --cov-report html"
