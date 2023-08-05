from setuptools import setup, find_packages

setup(
    name='motus',
    version='0.9.10.4',
    description='Paquetería para el Análisis Conductual de Patrones de Desplazamiento',
    author='Escamilla, Toledo, Tamayo, Avendaño, León, Eslava, Hernández',
    author_email='escamilla.een@gmail.com',
    packages=['motus', 'motus.fisica_estadistica', 'motus.graficador'],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'sklearn'
    ],
)