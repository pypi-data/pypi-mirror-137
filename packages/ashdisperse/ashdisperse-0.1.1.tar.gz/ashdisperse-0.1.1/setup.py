import setuptools
from distutils.util import convert_path

# from ashdisperse.utilities.utilities import utilities_cc
# from ashdisperse.spectral.cheb import cc as cheb_cc
# from ashdisperse.core.getters import cc as getters_cc
# from ashdisperse.core.core import cc as core_cc

main_ns = {}
ver_path = convert_path('ashdisperse/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name="ashdisperse",
    version=main_ns['__version__'],
    author="Mark Woodhouse",
    author_email="mark.woodhouse@bristol.ac.uk",
    description="Steady state advection-diffusion-sedimentation solver for volcanic ash dispersion",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # ext_modules=[
    #     utilities_cc.distutils_extension(),
    #     cheb_cc.distutils_extension(),
    #     getters_cc.distutils_extension(),
    #     core_cc.distutils_extension(),
    # ],
    install_requires=[
        'numpy',
        'numba',
        'scipy',
        'matplotlib',
        'netCDF4',
        'datetime',
        'utm',
        'rasterio',
        'scikit-image',
        'pandas',
        'geopandas',
        'shapely',
        'cdsapi',
        'prompt_toolkit',
        'siphon',
        'xarray',
        'rioxarray',
        'requests',
        'contextily',
        'osmnx',
        'geojsoncontour',
        'folium',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
