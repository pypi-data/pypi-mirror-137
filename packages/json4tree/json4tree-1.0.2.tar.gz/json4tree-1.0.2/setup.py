from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='json4tree',
    version='1.0.2',
    description="Makes any JSON compatible with D3's hierarchy or tree chart formats (see https://d3js.org)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/robertjamison/json4tree',
    author='Robert G. Jamison',
    author_email='info@robertjamison.us',
    license='MIT License',
    project_urls={
        "Bug Tracker": "https://github.com/robertjamison/json4tree/issues",
    },
    python_requires=">=3.0",
    packages=['json4tree'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
