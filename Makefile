.PHONY: install start test check
install:
	./install.sh
start:
	./run.sh
test:
	. .venv/bin/activate && python -m unittest discover -s tests -v
check:
	. .venv/bin/activate && python -m compileall -q backend && node --check app.js
