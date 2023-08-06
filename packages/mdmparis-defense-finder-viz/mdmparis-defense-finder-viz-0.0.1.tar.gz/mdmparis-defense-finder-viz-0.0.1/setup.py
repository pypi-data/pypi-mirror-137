from setuptools import setup
from setuptools.command.install import install

def read_md(f):
    import codecs
    with codecs.open(f, 'r', encoding='utf8') as f:
        text = f.read()
    return text

setup(name='mdmparis-defense-finder-viz',
        version='0.0.1',
        description="A helper tool to format data for defense-finder-web visualization from Prodigal and Defense Finder outputs.",
        long_description=read_md('README.md'),
        long_description_content_type="text/markdown",
        author="Alexandre Hervé",
        author_email="alexandreherve@protonmail.com",
        url="https://github.com/mdmparis/defense-finder",
        license="GPLv3",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
            ],
        python_requires='>=3.7',
        install_requires=[i for i in [l.strip() for l in open('requirements.txt').read().split('\n')] if i],
        packages=[
            'defense_finder_viz',
            'defense_finder_viz_cli',
        ],
        entry_points='''
          [console_scripts]
          defense-finder-viz=defense_finder_viz_cli.main:run
        '''
      )

