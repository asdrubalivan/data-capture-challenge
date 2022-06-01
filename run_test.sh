echo "Runnning pipenv shell";
pipenv shell;

echo "Running test coverage";
pipenv run test-coverage;
echo "Generating reports";
pipenv run coverage-report;
pipenv run coverage-html;

if [ "$1" == "--serve" ]; then
  pipenv run serve-coverage-html;
fi

