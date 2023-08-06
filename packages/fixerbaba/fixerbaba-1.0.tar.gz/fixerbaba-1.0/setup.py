import setuptools



with open("README.md", "r") as fh:

    long_description = fh.read()



setuptools.setup(

    name="fixerbaba", 

    version="1.0",

    author="BotolMehedi",

    author_email="Botol@email.com",

    description="Simple Tool For Fix B2K4 Error",

    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',

    url="https://github.com/BotolMehedi/b2k4",
    
    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 2",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=2.7',
    entry_points={'console_scripts': ['fixerbaba=fixerbaba.__init__:fixerbaba']}

)
