# ymedlop-db-memory-rest


oc login --insecure-skip-tls-verify=true
oc project bbva-offices

oc new-app --strategy=docker https://github.com/ymedlop/ymedlop-db-memory-rest.git

oc new-app --strategy=docker https://github.com/ymedlop/ymedlop-front-demo.git