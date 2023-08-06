""" Setup file """
from setuptools import setup, find_packages

REQUIREMENTS = [
    "semver==2.8.1",
    "python-gitlab==3.1.0",
    "ddt==1.4.4"
]

setup(
    name='semver_gitlab_dfx_test',
    version='0.0.1',
    description="Gitlab SEMVER Calculation CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    license='MIT',
    author="DefineX Labs",
    author_email='labs@teamdefinex.com.com',
    url="https://teamdefinex.com/",
    keywords="semver semantic versioning",
    platforms="any",
    zip_safe=False,
    python_requires=">=3.9",
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=REQUIREMENTS,
    setup_requires=REQUIREMENTS,
    test_suite='setup.my_test_suite',
)