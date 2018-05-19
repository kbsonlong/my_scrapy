#coding: utf-8

from flask_script import Manager,Server
import main

manager = Manager(main.app)

manager.add_command('server',Server())

@manager.shell
def make_shell_text():
    """Create a python CLI.

        return: Default import object
        type: `Dict`
        """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=main.app)


if __name__ == '__main__':
    manager.run()
