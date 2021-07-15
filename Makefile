

all: install exec clean

install: requirements.txt
	@python3 -m pip install -U -r requirements.txt

exec:
	@python3 src/main.py

clean:
	rm -r src/__pycache__
	@echo "Removed pycache files."