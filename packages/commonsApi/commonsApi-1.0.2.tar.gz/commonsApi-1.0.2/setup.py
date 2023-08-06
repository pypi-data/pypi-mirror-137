from setuptools import setup, find_packages
import codecs


try:
    with codecs.open( "README.md", 'r', errors='ignore' ) as file:
        readme_contents = file.read()

except Exception as error:
    readme_contents = ""
    sys.stderr.write( "Warning: Could not open README.md due %s\n" % error )

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Education'
]

setup(
    name="commonsApi",
    version="1.0.2",
    description="This is a package to automate apis in a simple way by using common reusable functions",
    long_description = readme_contents,
    long_description_content_type='text/markdown',
    url="https://github.com/ManikandanRajendran/python-package-for-api-testing",
    author="Manikandan Rajendran",
    author_email="r.manikandan.king@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=["api automation", "api testing", "api commons", "python api"],
    packages=find_packages(),
    install_requires=[
        "jsonschema==4.4.0",
        "requests==2.27.1"
        ]
)