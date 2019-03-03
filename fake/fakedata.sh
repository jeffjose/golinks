#!/bin/sh

curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/a
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/b
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/c
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/d
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/e
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/f
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/i
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/j
curl --request POST -H 'Content-Type: application/json' --data '{"destination":"google.com","creator":"xyz"}' http://localhost:8000/k
