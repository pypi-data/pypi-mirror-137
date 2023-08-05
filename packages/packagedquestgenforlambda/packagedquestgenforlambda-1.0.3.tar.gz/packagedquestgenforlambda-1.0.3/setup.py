from distutils.core import setup

setup(name='packagedquestgenforlambda',
      version='1.0.3',
      description='Question generator from any text',
      author='packagedquestgenforlambda contributors',
      author_email='vaibhavtiwarifu@gmail.com',
      packages=['packagedquestgenforlambda', 'packagedquestgenforlambda.encoding', 'packagedquestgenforlambda.mcq'],
      url="https://github.com/ramsrigouthamg/packagedquestgenforlambda.ai",
      install_requires=[
         
           'torch==1.9.0',
           'transformers==3.0.2',
           'pytorch_lightning==0.8.1',
           'sense2vec==1.0.3',
           'strsim==0.0.3',
           'six==1.15.0',
           'networkx==2.4.0',
           'numpy',
           'scipy',
           'scikit-learn',
           'unidecode==1.1.1',
           'future==0.18.2',
           'joblib==0.14.1',
           'spacy==2.2.4',
           'pytz==2020.1',
           'python-dateutil==2.8.1',
           'boto3==1.14.40',
           'flashtext==2.7',
           'pandas',
      ],
      package_data={'packagedquestgenforlambda': ['packagedquestgenforlambda.py', 'mcq.py', 'train_gpu.py', 'encoding.py']}
      )
