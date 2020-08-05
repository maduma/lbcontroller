from setuptools import setup

setup(
    name='lbcontroller',
    version='0.1',
    description='Loadbalancer controller',
    url='http://github.com/storborg/funniest',
    author='Stephane Nsakala',
    author_email='stephane.nsakala@luxairgroup.lu',
    license='MIT',
    packages=['lbcontroller'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['lbcontroller=lbcontroller.lbcli:main'],
    }
)
