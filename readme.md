# Terrene's Python SDK


## Development

### Install From Source

```
git clone git@github.com:terreneco/python-sdk.git
cd python-sdk
cmd/install
```

### Run Tests

To test the package run the following command:

```bash
python -m unittest terrene/tests.py
```

Make sure that you have the following environment variables set:

- `TERRENE_SDK_TEST_BASE_URL`
- `TERRENE_SDK_TEST_EMAIL`
- `TERRENE_SDK_TEST_PASSWORD`


## Get Started

```python
from terrene.contrib import Client

client = Client('https://<your-instance>.api.terrene.co')
client.authenticate_with_email_and_password('<email>', '<password>')
```

### Create a Reducer

```python
from terrene.store import BaseReducer

reducer = client.create(BaseReducer, dict(
    name='CSV Reducer Python SDK',
    description='CSV Reducer created by the python sdk',
    code='import pandas\ncontent = pandas.read_csv(content)'))

# test the reducer run method
dataframe, stderr = reducer.run(open('dist/titanic.csv'))
print(dataframe, stderr)
```

### Create a TFrame

```python
from terrene.store import TFrame

tframe = client.create(TFrame, dict(
    name='Titanic dataset tframe',
    description='some test tframe'))

background_job = tframe.from_reducer(reducer, open('dist/titanic.csv'))
while True:
    background_job.sync()
    if background_job.progress == 100 or background_job.failed:
        break
    time.sleep(1)

# print the loaded dataframe
tframe_df = tframe.download_dataframe()

# modify the tframe and upload it back
time.sleep(3)
tframe_df['New_Col'] = 'test'
background_job = tframe.upload_dataframe(tframe_df)
while True:
    background_job.sync()
    if background_job.progress == 100 or background_job.failed:
        break
    time.sleep(1)

```

### Create a Predictive Model

```python
from terene.model import PredictiveModel

model = client.create(PredictiveModel, dict(
    name='Titanic Predictive Model', description='Predictive Model',
    input_variables=['Age', 'Sex', 'Cabin', 'Parch'],
    output_variables=['Survived']))
suggested_trainers = model.suggest(tframe)

# display suggested_trainers
print(suggested_trainers)
```

```python
# train model with suggested trainer
background_job = model.train(tframe, suggested_trainers[0])
while True:
    background_job.sync()
    if background_job.progress == 100 or background_job.failed:
        break
    time.sleep(1)
```

```python
# test predictions
preds = model.predict({'Age': 12, 'Sex': 'male', 'Cabin': 'C30', 'Parch': 1})
print(preds)

# test batch predictions
time.sleep(2)
background_job = model.predict_from_tframe(tframe)
while True:
    background_job.sync()
    if background_job.progress == 100 or background_job.failed:
        break
    time.sleep(1)

# get the predicted tframe
time.sleep(2)
tframe_with_preds = tframe.download_dataframe()
print(tframe_with_preds)
```

### Send Notifications

All resources support sending notifications to users that have read, write, or execute access to them.

To send a warning to a TFrame do the following:

```python
tframe.warn(subject="Test Warning", content='Lorem ipsum....', target='read')  # target can be 'read', 'write', or 'execute'
```

To send a general notification do the following:

```python
tframe.inform(subject="Test Warning", content='Lorem ipsum....', target='read')  # target can be 'read', 'write', or 'execute'
```

Both warn and inform methods send notifications but `warn` has a higher priority and some users may have disabled
`info` notifications.

## Release

To release the package on pypi, install `twine` and do the following:

```bash
python setup.py sdist
twine upload --repository pypi dist/*.tar.gz
```

## License

Copyright 2018 Terrene, Inc.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
APARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
