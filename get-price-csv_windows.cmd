set PGPASSWORD=ergodex

psql -h localhost -p 5432 -d ergodex -U ergodex -f price-data.sql

psql -h localhost -p 5432 -d ergodex -U ergodex -f etl-price-data.sql

set PGPASSWORD=