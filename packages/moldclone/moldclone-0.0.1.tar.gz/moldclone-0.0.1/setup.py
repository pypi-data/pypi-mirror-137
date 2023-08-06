from setuptools import setup, find_packages
#AKXVAU
setup(
    name='moldclone',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.1",
    description='BD SMS BOMBER 2022',
    author='MOAJJEM',
    author_email='adethkhan@gmail.com',
    long_description=(open("README.md","r")).read(),
    long_description_content_type="text/markdown",
   install_requires=['requests'],
 
    keywords=['hacker', 'tool', 'prank', 'termux', 'hack','FB CLONE','CLONER', 'MOAJJEM', 'hack fb', 'facebook', 'cloning', 'python',  'python cloning', 'python2', 'python facebook crack','facebook', 'new cloner', 'facebook hack'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'moldclone = moldclone.moldclone:menu',
                
            ],
    },
    python_requires='>=3.9'
)

#TOXIC-VIRUS