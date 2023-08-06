# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightautoml',
 'lightautoml.addons',
 'lightautoml.addons.interpretation',
 'lightautoml.addons.uplift',
 'lightautoml.addons.utilization',
 'lightautoml.automl',
 'lightautoml.automl.presets',
 'lightautoml.dataset',
 'lightautoml.image',
 'lightautoml.ml_algo',
 'lightautoml.ml_algo.torch_based',
 'lightautoml.ml_algo.tuning',
 'lightautoml.pipelines',
 'lightautoml.pipelines.features',
 'lightautoml.pipelines.ml',
 'lightautoml.pipelines.selection',
 'lightautoml.reader',
 'lightautoml.report',
 'lightautoml.tasks',
 'lightautoml.tasks.losses',
 'lightautoml.text',
 'lightautoml.transformers',
 'lightautoml.utils',
 'lightautoml.validation']

package_data = \
{'': ['*'],
 'lightautoml.automl.presets': ['tabular_configs/*'],
 'lightautoml.report': ['lama_report_templates/*']}

install_requires = \
['autowoe>=1.2',
 'catboost',
 'cmaes',
 'dataclasses==0.6',
 'holidays',
 'jinja2',
 'joblib',
 'json2html',
 'lightgbm>=2.3,<3.0',
 'networkx',
 'optuna',
 'pandas>=1',
 'poetry-core>=1.0.0,<2.0.0',
 'pyyaml',
 'scikit-learn>=0.22',
 'scipy',
 'seaborn',
 'torch<1.9',
 'tqdm']

extras_require = \
{':python_full_version == "3.6.1" and sys_platform == "win32"': ['torch==1.7.0'],
 ':python_version < "3.7"': ['numpy>=1.11.1'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 ':python_version >= "3.7"': ['numpy>=1.20.0'],
 'all': ['gensim>=4',
         'nltk',
         'transformers>=4',
         'albumentations>=0.4.6',
         'efficientnet-pytorch',
         'opencv-python==4.5.2.52',
         'PyWavelets',
         'scikit-image',
         'torchvision',
         'weasyprint>=52.5,<53.0',
         'cffi>=1.14.5,<2.0.0'],
 'all:python_full_version == "3.6.1" and sys_platform == "win32"': ['torchvision==0.8.0'],
 'cv': ['albumentations>=0.4.6',
        'efficientnet-pytorch',
        'opencv-python==4.5.2.52',
        'PyWavelets',
        'scikit-image',
        'torchvision'],
 'cv:python_full_version == "3.6.1" and sys_platform == "win32"': ['torchvision==0.8.0'],
 'nlp': ['gensim>=4', 'nltk', 'transformers>=4'],
 'report': ['weasyprint>=52.5,<53.0', 'cffi>=1.14.5,<2.0.0']}

setup_kwargs = {
    'name': 'lightautoml',
    'version': '0.3.3',
    'description': 'Fast and customizable framework for automatic ML model creation (AutoML)',
    'long_description': '<img src=https://github.com/sberbank-ai-lab/LightAutoML/raw/master/imgs/LightAutoML_logo_big.png width=600 />\n\n# LightAutoML - automatic model creation framework\n\n[![Slack](https://lightautoml-slack.herokuapp.com/badge.svg)](https://lightautoml-slack.herokuapp.com)\n[![Telegram](https://img.shields.io/badge/chat-on%20Telegram-2ba2d9.svg)](https://t.me/lightautoml)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/lightautoml?color=green&label=PyPI%20downloads&logo=pypi&logoColor=orange&style=plastic)\n![Read the Docs](https://img.shields.io/readthedocs/lightautoml?style=plastic)\n![Tests](https://github.com/sberbank-ai-lab/LightAutoML/actions/workflows/CI.yml/badge.svg)\n\nLightAutoML (LAMA) is an AutoML framework by Sber AI Lab.\n\nIt provides automatic model creation for the following tasks:\n- binary classification\n- multiclass classification\n- regression\n\nCurrent version of the package handles datasets that have independent samples in each row. I.e. **each row is an object with its specific features and target**.\nMultitable datasets and sequences are a work in progress :)\n\n**Note**: we use [`AutoWoE`](https://github.com/sberbank-ai-lab/AutoMLWhitebox) library to automatically create interpretable models.\n\n**Authors**: [Alexander Ryzhkov](https://kaggle.com/alexryzhkov), [Anton Vakhrushev](https://kaggle.com/btbpanda), [Dmitry Simakov](https://kaggle.com/simakov), Vasilii Bunakov, Rinchin Damdinov, Pavel Shvets, Alexander Kirilin.\n\n**Documentation** of LightAutoML is available [here](https://lightautoml.readthedocs.io/), you can also [generate](https://github.com/sberbank-ai-lab/LightAutoML/blob/master/.github/CONTRIBUTING.md#building-documentation) it.\n\n<a name="toc"></a>\n# Table of Contents\n\n* [Installation LightAutoML from PyPI](#installation)\n* [Quick tour](#quicktour)\n* [Resources](#examples)\n* [Contributing to LightAutoML](#contributing)\n* [License](#apache)\n* [For developers](#developers)\n* [Support and feature requests](#support)\n\n<a name="installation"></a>\n# Installation\nTo install LAMA framework on your machine from PyPI, execute following commands:\n```bash\n\n# Install base functionality:\n\npip install -U lightautoml\n\n# For partial installation use corresponding option.\n# Extra dependecies: [nlp, cv, report]\n# Or you can use \'all\' to install everything\n\npip install -U lightautoml[nlp]\n\n```\n\nAdditionaly, run following commands to enable pdf report generation:\n\n```bash\n# MacOS\nbrew install cairo pango gdk-pixbuf libffi\n\n# Debian / Ubuntu\nsudo apt-get install build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info\n\n# Fedora\nsudo yum install redhat-rpm-config libffi-devel cairo pango gdk-pixbuf2\n\n# Windows\n# follow this tutorial https://weasyprint.readthedocs.io/en/stable/install.html#windows\n```\n[Back to top](#toc)\n\n<a name="quicktour"></a>\n# Quick tour\n\nLet\'s solve the popular Kaggle Titanic competition below. There are two main ways to solve machine learning problems using LightAutoML:\n* Use ready preset for tabular data:\n```python\nimport pandas as pd\nfrom sklearn.metrics import f1_score\n\nfrom lightautoml.automl.presets.tabular_presets import TabularAutoML\nfrom lightautoml.tasks import Task\n\ndf_train = pd.read_csv(\'../input/titanic/train.csv\')\ndf_test = pd.read_csv(\'../input/titanic/test.csv\')\n\nautoml = TabularAutoML(\n    task = Task(\n        name = \'binary\',\n        metric = lambda y_true, y_pred: f1_score(y_true, (y_pred > 0.5)*1))\n)\noof_pred = automl.fit_predict(\n    df_train,\n    roles = {\'target\': \'Survived\', \'drop\': [\'PassengerId\']}\n)\ntest_pred = automl.predict(df_test)\n\npd.DataFrame({\n    \'PassengerId\':df_test.PassengerId,\n    \'Survived\': (test_pred.data[:, 0] > 0.5)*1\n}).to_csv(\'submit.csv\', index = False)\n```\n\nLighAutoML framework has a lot of ready-to-use parts and extensive customization options, to learn more check out the [resources](#Resources) section.\n\n[Back to top](#toc)\n\n<a name="examples"></a>\n# Resources\n\n### Kaggle kernel examples of LightAutoML usage:\n\n- [Tabular Playground Series April 2021 competition solution](https://www.kaggle.com/alexryzhkov/n3-tps-april-21-lightautoml-starter)\n- [Titanic competition solution (80% accuracy)](https://www.kaggle.com/alexryzhkov/lightautoml-titanic-love)\n- [Titanic **12-code-lines** competition solution (78% accuracy)](https://www.kaggle.com/alexryzhkov/lightautoml-extreme-short-titanic-solution)\n- [House prices competition solution](https://www.kaggle.com/alexryzhkov/lightautoml-houseprices-love)\n- [Natural Language Processing with Disaster Tweets solution](https://www.kaggle.com/alexryzhkov/lightautoml-starter-nlp)\n- [Tabular Playground Series March 2021 competition solution](https://www.kaggle.com/alexryzhkov/lightautoml-starter-for-tabulardatamarch)\n- [Tabular Playground Series February 2021 competition solution](https://www.kaggle.com/alexryzhkov/lightautoml-tabulardata-love)\n- [Interpretable WhiteBox solution](https://www.kaggle.com/simakov/lama-whitebox-preset-example)\n- [Custom ML pipeline elements inside existing ones](https://www.kaggle.com/simakov/lama-custom-automl-pipeline-example)\n\n### Google Colab tutorials and [other examples](examples/):\n\n- `Tutorial_1_basics.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_1_basics.ipynb) - get started with LightAutoML on tabular data.\n- `Tutorial_2_WhiteBox_AutoWoE.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_2_WhiteBox_AutoWoE.ipynb) - creating interpretable models.\n- `Tutorial_3_sql_data_source.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_3_sql_data_source.ipynb) - shows how to use LightAutoML presets (both standalone and time utilized variants) for solving ML tasks on tabular data from SQL data base instead of CSV.\n- `Tutorial_4_NLP_Interpretation.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_4_NLP_Interpretation.ipynb) - example of using TabularNLPAutoML preset, LimeTextExplainer.\n- `Tutorial_5_uplift.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_5_uplift.ipynb) - shows how to use LightAutoML for a uplift-modeling task.\n- `Tutorial_6_custom_pipeline.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_6_custom_pipeline.ipynb) - shows how to create your own pipeline from specified blocks: pipelines for feature generation and feature selection, ML algorithms, hyperparameter optimization etc.\n- `Tutorial_7_ICE_and_PDP_interpretation.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sberbank-ai-lab/LightAutoML/blob/master/examples/tutorials/Tutorial_7_ICE_and_PDP_interpretation.ipynb) - shows how to obtain local and global interpretation of model results using ICE and PDP approaches.\n\n**Note 1**: for production you have no need to use profiler (which increase work time and memory consomption), so please do not turn it on - it is in off state by default\n\n**Note 2**: to take a look at this report after the run, please comment last line of demo with report deletion command.\n\n### Courses, videos and papers\n\n* **LightAutoML crash courses**:\n    - (Russian) [AutoML course for OpenDataScience community](https://ods.ai/tracks/automl-course-part1)\n\n* **Video guides**:\n    - (Russian) [LightAutoML webinar for Sberloga community](https://www.youtube.com/watch?v=ci8uqgWFJGg) ([Alexander Ryzhkov](https://kaggle.com/alexryzhkov), [Dmitry Simakov](https://kaggle.com/simakov))\n    - (Russian) [LightAutoML hands-on tutorial in Kaggle Kernels](https://www.youtube.com/watch?v=TYu1UG-E9e8) ([Alexander Ryzhkov](https://kaggle.com/alexryzhkov))\n    - (English) [Automated Machine Learning with LightAutoML: theory and practice](https://www.youtube.com/watch?v=4pbO673B9Oo) ([Alexander Ryzhkov](https://kaggle.com/alexryzhkov))\n    - (English) [LightAutoML framework general overview, benchmarks and advantages for business](https://vimeo.com/485383651) ([Alexander Ryzhkov](https://kaggle.com/alexryzhkov))\n    - (English) [LightAutoML practical guide - ML pipeline presets overview](https://vimeo.com/487166940) ([Dmitry Simakov](https://kaggle.com/simakov))\n\n* **Papers**:\n    - Anton Vakhrushev, Alexander Ryzhkov, Dmitry Simakov, Rinchin Damdinov, Maxim Savchenko, Alexander Tuzhilin ["LightAutoML: AutoML Solution for a Large Financial Services Ecosystem"](https://arxiv.org/pdf/2109.01528.pdf). arXiv:2109.01528, 2021.\n\n* **Articles about LightAutoML**:\n    - (English) [LightAutoML vs Titanic: 80% accuracy in several lines of code (Medium)](https://alexmryzhkov.medium.com/lightautoml-preset-usage-tutorial-2cce7da6f936)\n    - (English) [Hands-On Python Guide to LightAutoML – An Automatic ML Model Creation Framework (Analytic Indian Mag)](https://analyticsindiamag.com/hands-on-python-guide-to-lama-an-automatic-ml-model-creation-framework/?fbclid=IwAR0f0cVgQWaLI60m1IHMD6VZfmKce0ZXxw-O8VRTdRALsKtty8a-ouJex7g)\n\n[Back to top](#toc)\n\n<a name="contributing"></a>\n# Contributing to LightAutoML\nIf you are interested in contributing to LightAutoML, please read the [Contributing Guide](.github/CONTRIBUTING.md) to get started.\n\n[Back to top](#toc)\n\n<a name="apache"></a>\n# License\nThis project is licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/dev-rinchin/LightAutoML/blob/master/LICENSE) file for more details.\n\n[Back to top](#toc)\n\n<a name="developers"></a>\n# For developers\n\n## Installation from source code\n\nFirst of all you need to install [git](https://git-scm.com/downloads) and [poetry](https://python-poetry.org/docs/#installation).\n\n```bash\n\n# Load LAMA source code\ngit clone https://github.com/sberbank-ai-lab/LightAutoML.git\n\ncd LightAutoML/\n\n# !!!Choose only one item!!!\n\n# 1. Global installation: Don\'t create virtual environment\npoetry config virtualenvs.create false --local\n\n# 2. Recommended: Create virtual environment inside your project directory\npoetry config virtualenvs.in-project true\n\n# For more information read poetry docs\n\n# Install LAMA\npoetry lock\npoetry install\n```\n\n## Build your own custom pipeline:\n\n```python\nimport pandas as pd\nfrom sklearn.metrics import f1_score\n\nfrom lightautoml.automl.presets.tabular_presets import TabularAutoML\nfrom lightautoml.tasks import Task\n\ndf_train = pd.read_csv(\'../input/titanic/train.csv\')\ndf_test = pd.read_csv(\'../input/titanic/test.csv\')\n\n# define that machine learning problem is binary classification\ntask = Task("binary")\n\nreader = PandasToPandasReader(task, cv=N_FOLDS, random_state=RANDOM_STATE)\n\n# create a feature selector\nmodel0 = BoostLGBM(\n    default_params={\'learning_rate\': 0.05, \'num_leaves\': 64,\n    \'seed\': 42, \'num_threads\': N_THREADS}\n)\npipe0 = LGBSimpleFeatures()\nmbie = ModelBasedImportanceEstimator()\nselector = ImportanceCutoffSelector(pipe0, model0, mbie, cutoff=0)\n\n# build first level pipeline for AutoML\npipe = LGBSimpleFeatures()\n# stop after 20 iterations or after 30 seconds\nparams_tuner1 = OptunaTuner(n_trials=20, timeout=30)\nmodel1 = BoostLGBM(\n    default_params={\'learning_rate\': 0.05, \'num_leaves\': 128,\n    \'seed\': 1, \'num_threads\': N_THREADS}\n)\nmodel2 = BoostLGBM(\n    default_params={\'learning_rate\': 0.025, \'num_leaves\': 64,\n    \'seed\': 2, \'num_threads\': N_THREADS}\n)\npipeline_lvl1 = MLPipeline([\n    (model1, params_tuner1),\n    model2\n], pre_selection=selector, features_pipeline=pipe, post_selection=None)\n\n# build second level pipeline for AutoML\npipe1 = LGBSimpleFeatures()\nmodel = BoostLGBM(\n    default_params={\'learning_rate\': 0.05, \'num_leaves\': 64,\n    \'max_bin\': 1024, \'seed\': 3, \'num_threads\': N_THREADS},\n    freeze_defaults=True\n)\npipeline_lvl2 = MLPipeline([model], pre_selection=None, features_pipeline=pipe1,\n post_selection=None)\n\n# build AutoML pipeline\nautoml = AutoML(reader, [\n    [pipeline_lvl1],\n    [pipeline_lvl2],\n], skip_conn=False)\n\n# train AutoML and get predictions\noof_pred = automl.fit_predict(df_train, roles = {\'target\': \'Survived\', \'drop\': [\'PassengerId\']})\ntest_pred = automl.predict(df_test)\n\npd.DataFrame({\n    \'PassengerId\':df_test.PassengerId,\n    \'Survived\': (test_pred.data[:, 0] > 0.5)*1\n}).to_csv(\'submit.csv\', index = False)\n```\n\n[Back to top](#toc)\n\n<a name="support"></a>\n# Support and feature requests\nSeek prompt advice at [Slack community](https://lightautoml-slack.herokuapp.com) or [Telegram group](https://t.me/lightautoml).\n\nOpen bug reports and feature requests on GitHub [issues](https://github.com/sberbank-ai-lab/LightAutoML/issues).\n',
    'author': 'Alexander Ryzhkov',
    'author_email': 'AMRyzhkov@sberbank.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lightautoml.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
