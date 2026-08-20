.PHONY: pdf all clean

TECTONIC ?= $(shell which /Users/drb_laptop/.local/bin/tectonic 2>/dev/null || which tectonic 2>/dev/null || echo "tectonic")

all: pdf

pdf: main.pdf supplementary.pdf

main.pdf: main.tex references.bib npj-article.cls $(wildcard sections/*.tex) $(wildcard ../tables/*.tex) $(wildcard ../figures/*.pdf)
	@echo "==> Compiling npj Microgravity manuscript PDF..."
	$(TECTONIC) main.tex

supplementary.pdf: supplementary.tex references.bib npj-article.cls $(wildcard ../figures/*.pdf)
	@echo "==> Compiling Supplementary Information PDF..."
	$(TECTONIC) supplementary.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.pdf
