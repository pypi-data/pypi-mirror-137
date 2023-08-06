from setuptools import setup

setup(
    name='winotify',
    version='1.1.0.dev2',
    packages=["winotify"],
    url='https://github.com/versa-syahptr/winotify',
    license='MIT',
    author='versa',
    author_email='versa1220@gmail.com',
    description='Show notification toast on Windows 10',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['winotify=winotify.__main__:main'],
        'gui_scripts': ['winotify-nc=winotify.__main__:main']
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
