#! /bin/bash
npm run build
scp -r build/ ubuntu@sustainindyfoods.com:build/staged
ssh ubuntu@sustainindyfoods.com 'stat build/staged && rm -rf build/last &&  mv build/current build/last &&  mv build/staged build/current && sudo /snap/bin/docker exec saveourfaves-server_frontend_1 nginx -s reload'
