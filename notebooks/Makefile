CONVERTER=py2ipynb.py

.PHONY: all notebook

all: notebook

notebook:
	@curl -s -L https://raw.githubusercontent.com/yianni/py2ipynb/master/$(CONVERTER) -o $(CONVERTER)
	python $(CONVERTER) aggregated_crashes.py aggregated_crashes.ipynb
	@rm $(CONVERTER)
