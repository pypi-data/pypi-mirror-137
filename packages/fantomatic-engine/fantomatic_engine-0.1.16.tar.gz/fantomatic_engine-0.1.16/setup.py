from setuptools import setup, find_packages

setup(name="fantomatic_engine",
      version="0.1.16",
      description="A 2D top viewed game engine based on pygame",
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      url="https://gitlab.com/kuadrado-software/fantomatic-engine",
      author="Kuadrado Software",
      author_email="contact@kuadrado-software.fr",
      keywords='game 2d engine videogame',
      license="GNU-GPL-3.0",
      packages=find_packages(),
      install_requires=[
          "pygame==2.1.0",
          "numpy>=1.19.4",
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      python_requires='>=3.9',
      include_package_data=True,)
