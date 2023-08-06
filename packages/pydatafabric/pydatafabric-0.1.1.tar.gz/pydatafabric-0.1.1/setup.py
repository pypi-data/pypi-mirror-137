import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


# Start dependencies group
emart = [
    "bayesian-optimization==1.2.0",
    "catboost==1.0.3",
    "plotnine==0.8.0",
    "shap==0.40.0",
    "gensim==4.1.2",
    "seaborn==0.11.2",
    "scikit-learn==1.0.2",
    "scipy==1.7.3",
    "lifelines==0.26.4",
    "xgboost==1.5.1",
    "lightgbm==3.3.2",
    "implicit==0.4.8",
    "matplotlib==3.5.1",
    "mushroom_rl==1.7.0",
    "pytorch-widedeep==1.0.13",
    "RL-for-reco==1.0.27",
    "LightGBMwithBayesOpt==1.0.2",
    "tensorboardX==2.4.1",
    "torchsummary==1.5.1",
    "pycaret==2.3.6",
    "openpyxl>=3.0.0",
    "netcal",
]

setuptools.setup(
    name="pydatafabric",
    version="0.1.1",
    author="SHINSEGAE DataFabric",
    author_email="admin@shinsegae.ai",
    description="SHINSEGAE DataFabric Python Package",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/emartddt/dataplaltform-python-dist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "thrift-sasl==0.4.3",
        "hvac>=0.11.0",
        "pyhive[hive]==0.6.4",
        "pyarrow==6.0.1",
        "pandas==1.3.5",
        "slackclient>=2.9.0",
        "httplib2>=0.20.0",
        "click",
        "PyGithub",
        "pycryptodome",
        "tabulate>=0.8.0",
        "pandas_gbq>=0.16.0",
        "google-cloud-bigquery-storage==2.11.0",
        "grpcio==1.43.0",
        "sqlalchemy>=1.4.0",
        "packaging",
        "tqdm>=4.62.0",
        "ipywidgets",
        "hmsclient-hive-3",
        "google-cloud-bigtable==2.4.0",
        "google-cloud-monitoring==2.8.0",
        "redis",
    ],
    extras_require={"emart": emart},
)
