TYPE="$1"

is_user_root () { [ "$(id -u)" -eq 0 ]; }

check_cmd_success () {
	if [ $? -eq 0 ]; then
    echo "\n[#] DONE!\n"
	else
    echo "\n[#] FAIL!\n"
		exit 0
	fi
}

echo "[WARNING] Make sure to run script as root else script may fail!\n"

if [ ! -z "$TYPE" ]; then
	TYPE="--test"
fi

echo "[#] python3 setup.py install\n"
python3 setup.py install

check_cmd_success

echo "[#] python3 setup.py sdist bdist_wheel\n"
python3 setup.py sdist bdist_wheel

check_cmd_success

if "$TYPE" == "--live";then
	echo "[#] uploading to live server\n"
	twine upload dist/*
else
	echo "[#] uploading to test server\n"
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*	
fi

check_cmd_success