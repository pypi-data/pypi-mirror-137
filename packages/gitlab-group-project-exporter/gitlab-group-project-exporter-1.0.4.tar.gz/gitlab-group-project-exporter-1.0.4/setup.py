from setuptools import setup, find_packages

setup(
    name='gitlab-group-project-exporter',
    version='1.0.4',
    license='MIT',
    description='Export gitlab groups and projects for remote backups',
    author='Muhammad Asad',
    author_email='muhammad.asad@gmail.com',
    url='https://github.com/masad8',
    packages=find_packages(),
    scripts=["bin/main.py"],
    keywords=['Gitlab', 'Exporter', 'Backup'],
    install_requires=[
        'python-gitlab >= 3.1.1',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
