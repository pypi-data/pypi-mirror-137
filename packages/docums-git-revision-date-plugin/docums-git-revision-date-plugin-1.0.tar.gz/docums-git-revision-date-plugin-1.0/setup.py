from setuptools import setup, find_packages

setup(
    name='docums-git-revision-date-plugin',
    version='1.0',
    description='Docums plugin for setting revision date from git per markdown file.',
    keywords='docums git meta yaml frontmatter',
    url='https://github.com/khanhduy1407/docums-git-revision-date-plugin/',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=3.4',
    install_requires=[
        'docums>=1.0.0.0',
        'GitPython',
        'jinja2'
    ],
    packages=find_packages(),
    entry_points={
        'docums.plugins': [
            'git-revision-date = docums_git_revision_date_plugin.plugin:GitRevisionDatePlugin'
        ]
    }
)
