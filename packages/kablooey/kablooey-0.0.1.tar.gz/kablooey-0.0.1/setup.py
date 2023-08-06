import setuptools

long_description = open('descrip.md').read()
setuptools.setup(
    name="kablooey", # Put your package name here!
    version="0.0.1", # The version of your package!
    author="ShivC", # Your name here!
    author_email="system.io64@gmail.com", # Your e-mail here!
    description="Kaboom... in python. Original is in js", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kaboom-in-python.shivankchhaya.repl.co/site", # Link your package website here! (most commonly a GitHub repo)
    project_urls={
      'Documentation': 'https://kaboom-in-python.shivankchhaya.repl.co/docs',
    },
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8.2', # The version requirement for Python to run your package!
)