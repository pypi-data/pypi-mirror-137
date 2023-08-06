from distutils.core import setup
setup(
    # How you named your package folder (MyLib)
    name='gitlab-group-project-exporter',
    packages=['gitlabexporter'],   # Chose the same as "name"
    version='1.0.2',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Export gitlab groups and projects for backup',
    author='Muhammad Asad',                   # Type in your name
    author_email='muhammad.asad@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/masad8',
    # Keywords that define your package best
    keywords=['Gitlab', 'Exporter', 'Backup'],
    install_requires=[            # I get to this in a second
        'python-gitlab >= 3.1.1',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which python versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
