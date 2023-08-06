import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-private-asset-bucket",
    "version": "0.0.1",
    "description": "Construct to create a private asset S3 bucket. A cognito token can be used to allow access to he S3 asset.",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/cdk-private-asset-bucket",
    "long_description_content_type": "text/markdown",
    "author": "Martin Mueller<damadden88@googlemail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/cdk-private-asset-bucket"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_private_asset_bucket",
        "cdk_private_asset_bucket._jsii"
    ],
    "package_data": {
        "cdk_private_asset_bucket._jsii": [
            "cdk-private-asset-bucket@0.0.1.jsii.tgz"
        ],
        "cdk_private_asset_bucket": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-certificatemanager>=1.143.0, <2.0.0",
        "aws-cdk.aws-cloudfront-origins>=1.143.0, <2.0.0",
        "aws-cdk.aws-cloudfront>=1.143.0, <2.0.0",
        "aws-cdk.aws-cognito>=1.143.0, <2.0.0",
        "aws-cdk.aws-iam>=1.143.0, <2.0.0",
        "aws-cdk.aws-lambda-nodejs>=1.143.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.143.0, <2.0.0",
        "aws-cdk.aws-route53-targets>=1.143.0, <2.0.0",
        "aws-cdk.aws-route53>=1.143.0, <2.0.0",
        "aws-cdk.aws-s3>=1.143.0, <2.0.0",
        "aws-cdk.core>=1.143.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.52.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
