# 데이터 분석 및 시각화 도구

## 1. Usage
### 1.1 Install
```bash
$ pip install analysis-tools
```

## 1.2 Example code
```python
from analysis_tools.EDA.EDA import *


data_train = pd.read_csv(join(PATH.INPUT, 'train.csv'))
data_test  = pd.read_csv(join(PATH.INPUT, 'test.csv'))
data       = pd.concat([data_train, data_test])
data.set_index('PassengerId', inplace=True)
target_feature = 'Survived'

X, y = data.drop(columns=target_feature), data[target_feature]
eda = EDA(data, target=target_feature, save_path=PATH.RESULT)
ordinal_features = ['Pclass', 'SibSp', 'Parch']
nominal_features = ['Survived', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked']
eda.set_types(ord=ordinal_features, nom=nominal_features)
eda.run()
```

자세한 내용은 [examples/1_titanic/main.ipynb](examples/1_titanic/main.ipynb)를 참고
