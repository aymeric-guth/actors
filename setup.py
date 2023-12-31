from setuptools import setup, find_packages


setup(
    name="actors",
    version="0.0.1",
    license="GPLv2+",
    url="https://github.com/aymeric-guth/actors",
    description="Actor Model micro-framework",
    author_email="aymeric.guth@protonmail.com",
    author="Aymeric Guth",
    packages=find_packages(),
    install_requires=["utils @ git+https://github.com/aymeric-guth/utils@master"],
    package_data={"actors": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 or later(GPLv2+)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
