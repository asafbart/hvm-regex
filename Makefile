.PHONY: all test benchmark docs clean

all: test benchmark

test:
	./run_tests.sh

benchmark:
	./run_benchmarks.sh

docs:
	@echo "Documentation is in the docs/ directory"

clean:
	find . -name "*.hvm.out" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete