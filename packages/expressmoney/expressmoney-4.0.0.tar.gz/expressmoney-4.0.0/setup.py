"""
py setup.py sdist
twine upload dist/expressmoney-4.0.0.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='4.0.0',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('google-cloud-secret-manager', 'google-cloud-error-reporting', 'google-cloud-pubsub',
                      'google-cloud-tasks', 'requests', 'djangorestframework-simplejwt'),
    python_requires='>=3.7',
)
