from setuptools import setup

setup(
    name="fetch_aws_secrets_test",
    version="0.2",
    description="Use AWS defined function to fetch secrets",
    url="https://github.com/GioDecio/fetch_aws_secrets_test",
    author="Gpy",
    author_email="giovanni.decillis@gmail.com",
    license="private",
    packages=["fetch_aws_secrets_test"],
    install_requires=["boto3"],
    zip_safe=False,
)
