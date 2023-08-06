import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gym_wordle',
    version='0.1.0',
    author='David Kraemer',
    author_email='david.kraemer@stonybrook.edu',
    description='OpenAI gym environment for training agents on Wordle',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DavidNKraemer/Gym-Wordle',
    package_dir={'': 'gym_wordle'},
    packages=setuptools.find_packages(where='gym_wordle'),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
