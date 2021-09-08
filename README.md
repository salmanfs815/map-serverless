# map-serverless

Serverless API for Muslim Anthology Project website

## Setup Environment

```bash
virtualenv env
source env/Scripts/activate
pip install -r requirements.txt
```

## Run Locally (testing)

```bash
export FLASK_ENV=development
export FLASK_APP=application
flask run -h 0.0.0.0
```

## Deploy to AWS
```bash
zappa init
zappa deploy <stage>
```
