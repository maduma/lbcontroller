Middleware to control a loadbalancer
====================================

- Currently only working with apache loadbalancer
- Support basic authentication via environment variables LB_CREDS_USR and LB_CREDS_PSW

## Usage

```
Usage: lbcontroller [OPTIONS] COMMAND [ARGS]...

Options:
  --addr TEXT  loadbalancer address  [required]
  --http       force http, default is https
  --help       Show this message and exit.

Commands:
  disable
  enable
  status
```

# Example

```
$ lbcontroller --addr api-acc.in.luxair.lu status contact
Status for contact on api-acc.in.luxair.lu https loadbalancer: ('ok', ['Init Ok', 'Init Ok'])
$ lbcontroller --addr api-acc.in.luxair.lu disable contact 0
disable instance 0 of contact on api-acc.in.luxair.lu https loadbalancer
$ lbcontroller --addr api-acc.in.luxair.lu status contact
Status for contact on api-acc.in.luxair.lu https loadbalancer: ('degraded', ['Init Dis', 'Init Ok'])
$ lbcontroller --addr api-acc.in.luxair.lu enable contact 0
enable instance 0 of contact on api-acc.in.luxair.lu https loadbalancer
$ lbcontroller --addr api-acc.in.luxair.lu status contact
Status for contact on api-acc.in.luxair.lu https loadbalancer: ('ok', ['Init Ok', 'Init Ok'])

$ lbcontroller --addr api-acc.in.luxair.lu disable contact 1
disable instance 1 of contact on api-acc.in.luxair.lu https loadbalancer
$ lbcontroller --addr api-acc.in.luxair.lu status contact
Status for contact on api-acc.in.luxair.lu https loadbalancer: ('degraded', ['Init Ok', 'Init Dis'])
$ lbcontroller --addr api-acc.in.luxair.lu enable contact 1
enable instance 1 of contact on api-acc.in.luxair.lu https loadbalancer
$ lbcontroller --addr api-acc.in.luxair.lu status contact
Status for contact on api-acc.in.luxair.lu https loadbalancer: ('ok', ['Init Ok', 'Init Ok'])
```

## build and push docker image (e.g for v1.0.1)

```
$ docker build -t registry.in.luxair.lu/lbcontroller:v1.0.1 .
$ docker push registry.in.luxair.lu/lbcontroller:v1.0.1
```

## test and dev
- install python 3.8
- clone the git repo
- create a virtual env
- install python dependencies
- install the lbcontroller pkg localy
```
cd lbcontroller
python3.8 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
lbcontroller --help
```
- run unit test
```
pytest -vv
```
