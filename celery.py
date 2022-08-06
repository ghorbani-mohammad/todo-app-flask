from celery import Celery
from app import app as flask_app

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

flask_app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://prepare_4_redis:6379',
    'result_backend': 'redis://prepare_4_redis:6379',
})
celery = make_celery(flask_app)
