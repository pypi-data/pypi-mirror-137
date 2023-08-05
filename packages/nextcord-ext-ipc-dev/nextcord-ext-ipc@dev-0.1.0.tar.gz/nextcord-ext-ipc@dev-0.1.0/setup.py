import re
from distutils.core import setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()
    
packages = [
    'nextcord.ext.ipc',
]

project_urls = {
    "Issues": "https://github.com/japandotorg/nextcord-ext-ipc/issues",
    "Source": "https://github.com/japandotorg/nextcord-ext-ipc",
}

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

_version_regex = r"^version = ('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"

with open("nextcord/ext/ipc/__init__.py") as f:
    match = re.search(_version_regex, f.read(), re.MULTILINE)
    
version = match.group(2)

if match.group(3) is not None:
    try:
        import subprocess
        
        process = subprocess.Popen(["git", "rev-list", "--count", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += out.decode("utf-8").strip()
            
        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except (Exception) as e:
        pass
    
setup(
    name='nextcord-ext-ipc@dev',
    author='japandotorg',
    python_requires='>=3.8.0',
    url='',
    version=version,
    project_urls=project_urls,
    packages=packages,
    license='MIT',
    description='A nextcord extension for ipc server.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=install_requires,
    keywords=[
        'nextcord',
        'extension',
        'ipc-server'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)