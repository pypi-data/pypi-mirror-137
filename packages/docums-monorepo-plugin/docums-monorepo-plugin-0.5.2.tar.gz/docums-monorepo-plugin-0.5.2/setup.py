import setuptools


setuptools.setup(
    name='docums-monorepo-plugin',
    version='0.5.2',
    description='Plugin for adding monorepository support in Docums.',
    long_description="""
        This introduces support for the !include syntax in docums.yml, allowing you to import additional Docums navigation.
        It enables large or complex repositories to have their own sets of docs/ folders, whilst generating only a single Docums site.
        This is built and maintained by the engineering community at Spotify.
    """,  # noqa: E501
    keywords='docums monorepo',
    url='https://github.com/khanhduy1407/docums-monorepo-plugin',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='Apache-2.0',
    python_requires='>=3',
    install_requires=[
        'docums>=1.0.0.0',
        'python-slugify>=4.0.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'docums.plugins': [
            "monorepo = docums_monorepo_plugin.plugin:MonorepoPlugin"
        ]
    }
)
