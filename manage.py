import json
import logging
import os
import unittest

from flask_script import Manager
from app import blueprint, create_app

app = create_app()
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=5200)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def coverage():
    """Checks the coverage."""
    try:
        min_coverage = 70
        cmd_test = "coverage run --source='.' manage.py test &&"
        cmd_coverage = "&& coverage report && coverage json"
        os.system(
            cmd_test+cmd_coverage)
        cov_json = json.loads(open('coverage.json', 'r').read())
        covered = cov_json['totals']['percent_covered']
        assert covered > min_coverage
        return 0
    except AssertionError:
        logging.error(
            'Not enough coverage: {covered}. Minimum coverage: {min_coverage}')
        return 1
    except Exception:
        logging.exception('Error running coverage')
        return 1


if __name__ == '__main__':
    manager.run()
