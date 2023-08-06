import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmc_mesh_tally_to_vtk",
    version="0.2.1",
    author="The Regular Mesh Plotter Development Team",
    author_email="mail@jshimwell.com",
    description="A Python package for converting OpenMC mesh tallies to VTK files and optionally converting the units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/openmc_mesh_tally_to_vtk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "openmc_mesh_tally_to_vtk": [
            # "requirements.txt",
            "README.md",
            "LICENSE",
        ]
    },
    install_requires=[
        "numpy>=1.21.1",
        "matplotlib>=3.4.2",
        "trimesh",
        "shapely",
        "scipy",
        "dagmc_geometry_slice_plotter",
        "openmc_tally_unit_converter",
        "vtk",
    ],
)
