.PHONY: all examples verify clean

all: examples verify

examples:
	python3 scripts/extract_examples.py

verify:
	python3 scripts/verify_examples.py

clean:
	rm -rf examples/
