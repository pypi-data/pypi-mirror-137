from setuptools import setup, find_packages


setup(
    name='docums-tooltipster-links-plugin',
    version='0.1.0',
    description='An Docums plugin',
    long_description='An Docums plugin that adds tooltips to preview the content of page links using tooltipster',
    keywords='docums',
    url='https://github.com/khanhduy1407/docums-tooltipster-links-plugin',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'docums>=1.0.0.0',
        'beautifulsoup4>=4.8.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'docums.plugins': [
            'tooltipster-links = docums_tooltipster_links_plugin.plugin:TooltipsterLinks'
        ]
    }
)
