import pathlib
from setuptools import setup
import pkg_resources

with pathlib.Path('requirements.txt').open() as f:
    install_requires = [str(r) for r in pkg_resources.parse_requirements(f)]

setup(name='sust-api-client',
      description='Sust Global API Client',
      packages=[
        'sust.api',
        'sust.api.generated',
        'sust.api.generated.climate_explorer',
        'sust.api.generated.climate_explorer.api',
        'sust.api.generated.climate_explorer.apis',
        'sust.api.generated.climate_explorer.model',
        'sust.api.generated.climate_explorer.models',
      ],
      install_requires=[install_requires],
)
