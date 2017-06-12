# Aloísio Imóveis

System to insert and search for properties inside the Aloísio Imóveis real estate website.


## How to develop?

1. Clone the repository
2. Create a virtualenv with Python 3.5
3. Activate your virtualenv
4. Install the dependencies
5. Set up the instance with the .env file
6. Run the tests

```console
git clone git@github.com:thiagorossener/aloisioimoveis.git aloisioimoveis
cd aloisioimoveis
python -m venv .aloisioimoveis
source .aloisioimoveis/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```
