.PHONY: dev
dev:
	python src/main.py --mode=dev

.PHONY: prod
prod:
	python src/main.py --mode=prod
