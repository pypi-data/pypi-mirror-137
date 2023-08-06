from setuptools import setup

setup(
    name='termact',
    description="Clear the terminal with termact.clear()",
    long_description="""
# Terminal lib for Python
Its awesome go go ahead and use ```pip install termact```

# Usage
To clear the terminal (this works on Windows, Mac, and Linux!), use ```termact.clear()``` and it should clear the terminal
""",
    long_description_content_type="text/markdown",
    version='0.0.1',
    packages=['termact'],
    #url="https://github.com/s4300/termact",
    install_requires=[
        #'os',
        'importlib; python_version == "2.6"',
    ],
)