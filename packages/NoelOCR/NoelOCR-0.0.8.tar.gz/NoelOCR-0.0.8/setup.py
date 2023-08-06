from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='NoelOCR',
    version = '0.0.8',
    description = 'Python Optical Character Recognition based libray for text extraction of scanned PDF',
    long_description=open('README.txt').read(),
    url = '',
    author = 'Noel Moses Mwadende',
    author_email='mosesnoel02@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Opctical Character Recognition,Scanned PDF, PDF Text Extraction, OCR',
    packages=find_packages(),
    install_requires = ['Pillow==9.0.1', 'pytesseract==0.3.8', 'Wand==0.6.7']
)
