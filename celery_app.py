from .app import app
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.conf.broker_url = 'redis://prepare_4_redis:6379'
    celery.conf.result_backend = 'redis://prepare_4_redis:6379'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)