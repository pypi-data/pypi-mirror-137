import versioneer
from setuptools import setup


with open('requirements.txt', 'r') as file:
    REQUIREMENTS = file.readlines()

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='drb-topic-safe',
    description='Safe topic for DRB Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/topics/safe',
    python_requires='>=3.8',
    install_requires=REQUIREMENTS,
    packages=['drb_topic_safe'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    package_data={'drb_topic_safe': ['cortex.yml']},
    data_files=[('.', ['requirements.txt'])],
    entry_points={'drb.impl': ['safe=drb_topic_safe']},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
