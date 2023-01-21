#!/bin/bash

docker run -d --name pri_solr -p 8983:8983 solr:8.10

docker exec pri_solr bin/solr create_core -c pri_solr_ngrams -p 8983

docker exec pri_solr bin/solr create_core -c pri_solr_bad

docker exec pri_solr bin/solr create_core -c pri_solr_final

docker cp ./solr/synonyms.txt pri_solr:/var/solr/data/pri_solr_ngrams/data/synonyms.txt
docker cp ./solr/synonyms.txt pri_solr:/var/solr/data/pri_solr_bad/data/synonyms.txt
docker cp ./solr/synonyms.txt pri_solr:/var/solr/data/pri_solr_final/data/synonyms.txt
docker cp ./solr/solrconfig.xml pri_solr:/var/solr/data/pri_solr_final/conf/solrconfig.xml
docker cp ./solr/jetty.xml pri_solr:/opt/solr-8.10.1/server/etc/jetty.xml

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @./solr/schema_final.json \
    http://localhost:8983/solr/pri_solr_final/schema

# Data definition via API
curl -X POST -H 'Content-type:text/csv' \
    --data-binary @../pipeline/out/csv_data/clean/full_final_solr.csv \
    http://localhost:8983/solr/pri_solr_final/update?commit=true

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @./solr/schema_ngrams.json \
    http://localhost:8983/solr/pri_solr_ngrams/schema

# Data definition via API
curl -X POST -H 'Content-type:text/csv' \
    --data-binary @../pipeline/out/csv_data/clean/final_solr.csv \
    http://localhost:8983/solr/pri_solr_ngrams/update?commit=true

# Data definition via API
curl -X POST -H 'Content-type:text/csv' \
    --data-binary @../pipeline/out/csv_data/clean/final_solr.csv \
    http://localhost:8983/solr/pri_solr_bad/update?commit=true

docker exec -u 8983 -it pri_solr bin/solr restart

sleep 2

docker start pri_solr
