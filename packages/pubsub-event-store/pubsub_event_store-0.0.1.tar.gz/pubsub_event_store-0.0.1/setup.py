import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pubsub_event_store",
    version="v0.0.1",
    install_requires=[
        "django==3.2.11",
        "django-model-utils==4.0.0",
        "djangorestframework==3.11.2",
        "django-environ==0.4.5",
    ],
    author="Anmol Porwal",
    author_email="anmolporwal@ymail.com",
    description="Saving event details to be able to replay them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Anmol-Porwal18/pubsub_event_store",
    platforms=["any"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(exclude=("sample",)),
    python_requires=">=3.7",
    keywords=["events", "rabbitmq", "replay events", "pubsub"],
)
