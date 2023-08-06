# Canopy

Social web platform

![Demo](https://media.githubusercontent.com/media/canopy/canopy/main/demo.gif)

## Use

[Linux](https://github.com/canopy/canopy/releases/download/v0.0.1-alpha/gaea) |
Windows |
Mac

## Develop

```shell
git clone https://github.com/canopy/canopy.git && cd canopy
# manually remove relative dev dependencies from pyproject.toml
poetry install
WEBCTX=dev poetry run web serve canopy:app --port 9000
# hack
poetry run build_gaea  # optional
```
