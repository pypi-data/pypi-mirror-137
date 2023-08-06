import setuptools

VERSION = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="happychat",
    version=VERSION,
    author="Jiri Kacirek",
    author_email="kacirek.j@gmail.com",
    description="Unsecure chatting app using email.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kacirekj/happychat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['happychat=happychat.happychat:main'],
    },
    install_requires=[
        'mailthon', ' imap-tools'
    ],
)
