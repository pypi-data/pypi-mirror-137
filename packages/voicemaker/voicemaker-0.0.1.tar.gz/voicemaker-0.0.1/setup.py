from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A Voicemaker.in simple API interface'
LONG_DESCRIPTION = 'Voicemaker.in is an online text-to-speech service with a dead-simple API. This package is just a wrapper around their API. This is an unofficial package, and is in no way associated to Voicemaker.'

# Setting up
setup(
        name="voicemaker", 
        version=VERSION,
        author="Adrian Castro",
        author_email="<adrian.d.castro.t@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["requests"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'tts', 'voicemaker', 'api'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
