from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7'
]

setup(
    name='robloxapiwrapper',
    version='0.9.1.1',
    description='Roblox Api Wrapper',
    ong_description_content_type=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Charlie Brasso',
    author_email='charliebrasso20@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='roblox', 
    packages=find_packages(),
    install_requires=['requests', 'discord_webhook'] 
)
