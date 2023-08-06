from distutils.core import setup
import os
import setuptools

def read(rel_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_path, rel_path), 'r') as f:
        return f.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError('Unable to find version string.')


if __name__ == '__main__':
    setuptools.setup(
        name='pytorch-fxdt1',
        version=get_version(os.path.join('src', 'pytorch_fxdt1', '__init__.py')),
        author='Akshaya Karthikeyan',
        author_email='akshaya.karthikeyan@research.iiit.ac.in',
        license='MIT',
        description=('A package containing methods to compute FXD score and other popular metrics for Chest X-Rays.'),
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        url='https://github.com/Akshayakayy/FXD_Score.git',
        download_url = 'https://github.com/Akshayakayy/FXD_Score/archive/refs/tags/0.1.tar.gz',
        keywords = ['FXD', 'Evaluation metric', 'featurization'],
        package_dir={'': 'src'},
        packages=setuptools.find_packages(where='src'),
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'License :: OSI Approved :: MIT License',
        ],
        python_requires='>=3.5',
        entry_points={
            'console_scripts': [
                'pytorch-fxdt1 = pytorch_fxdt1.fxd_score:main',
            ],
        },
        install_requires=[
            "setuptools>=42",
            "wheel",
            "numpy",
            "scipy",
            "pytorch-fid",
            "torch",
            "scikit-image",
            "matplotlib",
            "torchxrayvision",
            "torchvision",
            "sklearn",
            "tqdm",
        ],
#         extras_require={'dev': ['flake8',
#                                 'flake8-bugbear',
#                                 'flake8-isort',
#                                 'nox']},
    )