# ymedlop-db-memory-rest



 docker build -t ymedlop/ymedlop-deb-memory-rest .
 docker run -p 5000:5000 --name offices ymedlop/ymedlop-deb-memory-rest

oc login --insecure-skip-tls-verify=true
oc project bbva-offices

oc new-app --strategy=docker https://github.com/ymedlop/ymedlop-db-memory-rest.git

oc new-app --strategy=docker https://github.com/ymedlop/ymedlop-front-demo.git