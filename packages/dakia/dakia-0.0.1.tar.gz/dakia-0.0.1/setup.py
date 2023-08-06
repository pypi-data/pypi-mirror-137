from setuptools import setup, find_packages

with open("README.md", 'r',encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='dakia',
    version='0.0.1',
    author='Allwyn Fernandes',
    author_email='thisallwyn@gmail.com',
    description='Send yourself real time alerts and update messages about your projects on any platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # py_modules=['dakia'],
    url='https://github.com/allwynfernandes/dakia',
    install_requires=["requests"],
    keywords=['logging', 'updates', 'alerts', 'debug', 'notification'],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Communications :: Chat",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Education",
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 1 - Planning",
    ],

    package_dir={"":"src"},
    packages=find_packages(where='src'),
    python_requires='>=3.6',


)