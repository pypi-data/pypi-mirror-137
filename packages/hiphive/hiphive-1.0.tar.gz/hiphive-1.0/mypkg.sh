# More information available on
# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# https://docs.python.org/3/extending/building.html

# clean up
rm -fr build/ dist/ *.egg-info/ tmp/

# prepare source distribution and wheel
python3 setup.py sdist
python3 setup.py bdist_wheel --universal

# FIRST TESTING
# upload to test.pypi.org
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# test install
python3 -m pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    hiphive

# AFTER TESTING
# upload to actual index
#twine upload dist/*
