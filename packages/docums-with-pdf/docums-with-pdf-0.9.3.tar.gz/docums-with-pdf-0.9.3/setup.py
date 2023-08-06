import io

from setuptools import find_packages, setup

setup(
    name='docums-with-pdf',
    version='0.9.3',
    description='Generate a single PDF file from Docums repository',  # noqa E501
    long_description=io.open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='docums pdf weasyprint',
    url='https://github.com/khanhduy1407/docums-with-pdf',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'docums>=1.1.0',
        'weasyprint>=0.44',
        'beautifulsoup4>=4.6.3',
        'libsass>=0.15'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'docums.plugins': [
            'with-pdf = docums_with_pdf.plugin:WithPdfPlugin'
        ]
    }
)
