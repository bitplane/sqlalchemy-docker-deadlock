Example of deadlock under postgres in sqlalchemy when using engine.execute(ddl)
and session.execute(dql) within a short period of time.

Requires docker, python3, pip

run `./run.sh`, cry your eyes out.

then `docker ps` and `docker stop` the process to break the lock
