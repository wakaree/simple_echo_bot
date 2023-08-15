
package_dir := bot

.PHONY: lint
lint:
	black --check $(package_dir)
	ruff $(package_dir)
	mypy $(package_dir) --strict

.PHONY: reformat
reformat:
	black $(package_dir)
	ruff $(package_dir) --fix
