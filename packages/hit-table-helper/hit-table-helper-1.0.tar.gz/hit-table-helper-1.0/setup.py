import os

from setuptools import setup, find_packages


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires

p = find_packages()
print(p)

setup(
    name='hit-table-helper',
    version='1.0',
    url='https://git.hit.edu.cn/Chemie13/hit-table-helper',
    license='MIT',
    author='Y.C. Long',
    author_email='847072154@qq.com',
    install_requires=_process_requirements(),
    description='Course table helper for Harbin Institute of Technology.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    packages=p,
    python_requires='>=3.8, <4',
    keywords=['chemistry','analytical chemistry']
)

