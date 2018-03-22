# Terrene's Python SDK

Please visit [Terrene's python docs](https://docs.terrene.co/?python) 
to get started.


## Development

### Install From Source

```
git clone https://git.terrene.co/open-source/terrene-python-sdk
cd python-sdk
cmd/install
```

### Run Tests

To test the package run the following command:

```bash
export EMAIL=<your_email>; export PASSWORD=<your_password>; cmd/test
```


### Update the package

To update to the latest version run the following command:

```bash
cmd/update
```


## Authentication

To authenticate your api client, first set email and password environment variables:

```bash
export EMAIL=<your_email>; 
export PASSWORD=<your_password>;
```

Then use EmailPasswordCredentials to enable access to your account:

```
EmailPasswordCredentials(
    email=os.environ.get('EMAIL'), 
        password=os.environ.get('PASSWORD'))
```

Note, you only need to authenticate with this method once. All the other SDK methods will use automatically 
use your authenticated credentials

## License

Copyright 2017 Terrene, Inc.

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
