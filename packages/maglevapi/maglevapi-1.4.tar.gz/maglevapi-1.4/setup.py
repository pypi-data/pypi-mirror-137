from distutils.core import setup

install_requires = [
    "termcolor",
    "bcrypt",
    "flask[async]"
]


setup(
    name="maglevapi",
    packages=["maglevapi", "maglevapi.flask_utils",
              "maglevapi.os_interface", "maglevapi.testing"],
    version="1.4",
    license="MIT",
    description="This is a personal library that I've developed that has a collection of functions and classes that allows me to develop new programs much much faster.",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/maglevapi",
    download_url="https://github.com/bossauh/maglevapi/archive/refs/tags/1_4.tar.gz",
    keywords=["helper", "toolkit"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
