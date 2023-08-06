from setuptools import setup, find_packages


setup(
    name='docums-awesome-pages-plugin',
    version='2.6.1',
    description='An Docums plugin that simplifies configuring page titles and their order',
    long_description='The awesome-pages plugin allows you to customize how your pages show up the navigation of your '
                     'Docums without having to configure the full structure in your ``docums.yml``. It gives you '
                     'detailed control using a small configuration file directly placed in the relevant directory of '
                     'your documentation. See `Github <https://github.com/khanhduy1407/docums-awesome-pages-plugin>`_ '
                     'or the README.md for more details.',
    keywords='docums python markdown wiki',
    url='https://github.com/khanhduy1407/docums-awesome-pages-plugin/',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'docums>=1.0.0.0',
        'wcmatch>=7'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    entry_points={
        'docums.plugins': [
            'awesome-pages = docums_awesome_pages_plugin.plugin:AwesomePagesPlugin'
        ]
    }
)
