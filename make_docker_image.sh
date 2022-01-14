#!/bin/bash
## sole parameter is an integer indicating incremental daily version
BUILD_TAG=dbcawa/boranga:v$(date +%Y.%m.%d).$1
git checkout dbca_dev &&
git pull &&
cd boranga/frontend/boranga/ &&
npm run build &&
cd ../../../ &&
source venv/bin/activate &&
./manage.py collectstatic --no-input &&
git log --pretty=medium -30 > ./ll_git_history &&
docker image build --no-cache --tag $BUILD_TAG . &&
git checkout working
echo $BUILD_TAG
