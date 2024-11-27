# Publish poetry packages
cd poetry/pkg_p1
poetry publish --build --repository private-pypi

cd ../pkg_p2
poetry publish --build --repository private-pypi
