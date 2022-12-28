import click
import os
import sys
from flask_babel import gettext as _
from app import create_app
from app.extensions import db
from app.models import Role, User, Contactor, Customer, Notification, Message, Task, \
    Visit, City, Province, Attachment, Visittype, Team, Order, Orderrec, Workflow, Node, Address
from config import Config


from flask import request

app = create_app(Config)
# print(app.url_map)


# 创建 coverage 实例
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.route('/')
def hello_world():
    return _('Hello, World!')


@app.shell_context_processor
def make_shell_context():
    return {
    'db': db,
    'Role': Role,
    'User': User,
    'Contactor': Contactor,
    'Customer': Customer,
    'Notification': Notification,
    'Message': Message,
    'Task': Task,
    'Visit': Visit,
    'City': City,
    'Province': Province,
    'Attachment': Attachment,
    'Visittype': Visittype,
    'Team': Team,
    'Order': Order,
    'Orderrec': Orderrec,
    'Workflow': Workflow,
    'Node': Node,
    'Address': Address
    }


@app.cli.command()
def deploy():
    '''Run deployment tasks.'''
    #  初始化测试数据
    Role.insert_roles()
    Province.init_data()
    City.init_data()
    Team.init_data()
    User.init_data()
    Workflow.init_data()
    Node.init_data()
    Customer.init_data()
    Contactor.init_data()
    Visittype.init_data()
    Address.init_data()

    users = User.query.all()
    for u in users:
        if u.username == 'miaohf':
            pass
        elif u.username in ['zhangsan', 'lisi'] :
            u.set_password('123456')
            u.role_id = 3
        else:
            u.set_password('123456')
            u.role_id = 2
    db.session.commit()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test(coverage):
    '''Run the unit tests.'''
    # 如果执行 flask test --coverage，但是FLASK_COVERAGE环境变量不存在时，给它配置上
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'  # 需要字符串的值
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(os.path.join(basedir, 'tmp'), 'coverage')
        COV.html_report(directory=covdir)
        print('')
        print('HTML report be stored in: %s' % os.path.join(covdir, 'index.html'))
        COV.erase()


@app.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404 