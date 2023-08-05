from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apptrail-application-events-sdk",
    version="0.0.2",
    author="Apptrail Team",
    author_email="support@apptrail.com",
    description="Apptrail Application Events SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://apptrail.com",
    project_urls={
        "SDK Reference": "https://apptrail.com/docs/applications/guide/working-with-events/using-the-events-sdk/application-events-sdk-python",
        "Developer Guide": "https://apptrail.com/docs/applications/guide",
        "Apptrail Docs": "https://apptrail.com/docs",
    },
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data = {
        'apptrail_application_events_sdk': ['py.typed', "raw-event-schema.json"],
    },
    #include_package_data=True,
    keywords=["apptrail", "apptrail events SDK", "audit logs", "audit trails", "apptrail application events SDK"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Logging",
        "Topic :: Security",
    ],
    setup_requires=["setuptools-git"],
    install_requires=[
        "requests",
        "backoff",
        "jsonschema[format_nongpl]",
        "jsonlines",
    ],
    python_requires=">=3.6",
)
