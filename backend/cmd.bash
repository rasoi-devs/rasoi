# !/bin/bash
# https://stackoverflow.com/a/24049420
# use these to create and download dataset generated inside a cloud vm (like aws ec2)

pg_dump -h localhost -U postgres -Fc -Z 9  --file=rasoi1_quick.dump rasoi1

pg_restore -h localhost -U postgres -Fc -j 8 rasoi1_quick.dump

# to run server:
pip install poetry (if you don't have it installed)
poetry install
poetry run pip install tensorflow
poetry run app.main