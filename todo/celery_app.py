from app import app
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])
    celery.conf.broker_url = "redis://todo_redis:6379"
    celery.conf.result_backend = "redis://todo_redis:6379"

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_CONFIG={
        "broker_url": "redis://todo_redis:6379",
        "result_backend": "redis://todo_redis:6379",
    }
)
celery = make_celery(app)
