from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from app import create_app
from exts import db
from apps.cms import models as cms_models


CMSUser = cms_models.CMSUser
app = create_app()

manager = Manager(app)

Migrate(app,db)
manager.add_command("db", MigrateCommand)

@manager.option("-u", "--username", dest="username")
@manager.option("-p", "--password", dest="password")
@manager.option("-e", "--email", dest="email")
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户创建成功")

@manager.command
def create_role():
    visitor = cms_models.CMSRole(name="访问者", intro="允许访问相关个人页面")
    visitor.permission = cms_models.CMSPermission.VISITOR

    operator = cms_models.CMSRole(name="运营", intro="管理帖子，评论与用户")
    operator.permission = cms_models.CMSPermission.VISITOR|cms_models.CMSPermission.POSTER|\
                          cms_models.CMSPermission.COMMENTER|cms_models.CMSPermission.FRONTUSER

    admin = cms_models.CMSRole(name="管理员", intro="所有权")
    admin.permission = cms_models.CMSPermission.VISITOR|cms_models.CMSPermission.POSTER|\
                       cms_models.CMSPermission.COMMENTER|cms_models.CMSPermission.FRONTUSER|\
                       cms_models.CMSPermission.BOARDER|cms_models.CMSPermission.CMSUSER

    developer = cms_models.CMSRole(name="开发者", intro="开发专用")
    developer.permission = cms_models.CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

@manager.option("-e", "--email", dest="email")
@manager.option("-n", "--name", dest="name")
def add_user_to_role(email, name):
    user = cms_models.CMSUser.query.filter_by(email=email).first()
    if user:
        role = cms_models.CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("添加角色成功")
        else:
            print("没有这个角色：%s"%role)
    else:
        print("该用户不存在。邮箱：%s"%email)

if __name__ == "__main__":
    manager.run()