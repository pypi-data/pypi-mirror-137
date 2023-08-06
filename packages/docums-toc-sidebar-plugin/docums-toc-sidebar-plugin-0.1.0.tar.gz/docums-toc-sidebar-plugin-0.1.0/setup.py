from setuptools import setup, find_packages


setup(
    name='docums-toc-sidebar-plugin',
    version='0.1.0',
    description='An Docums plugin',
    long_description='An Docums plugin that allows users to add additional content to the ToC sidebar using the Material theme',
    keywords='docums',
    url='https://github.com/khanhduy1407/docums-toc-sidebar-plugin',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'docums>=1.0.0.0',
        'docurial>=8.1.8.1',
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
            'toc-sidebar = docums_toc_sidebar_plugin.plugin:TocSidebar'
        ]
    }
)
