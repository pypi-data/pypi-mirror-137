from setuptools import setup

long_description = 'audioevaluator is a simple, easy-to-use supporting package for Earudite designed for performing ' \
                   'ASR on audios to determine their quality relative to a transcript. '

# specify requirements of your package here
REQUIREMENTS = ['jiwer==2.3.0'
    , 'numpy==1.22.1'
    , 'python-Levenshtein==0.12.2'
    , 'torch==1.10.0'
    , 'torchaudio==0.10.0'
    , 'typing_extensions==4.0.1'
                ]

# some more details
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
]

# calling the setup function
setup(name='audio-evaluator',
      version='1.0.6',
      description='A PyTorch wrapper for ASR and Earudite',
      long_description=long_description,
      author='Shivam Malhotra and Andrew Chen',
      author_email='alchen2@andrew.cmu.edu',
      url='https://github.com/achen4290/audio-evaluator',
      license='MIT',
      packages=['audioevaluator'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='asr audio pytorch'
      )
