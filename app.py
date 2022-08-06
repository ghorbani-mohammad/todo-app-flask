from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, marshal_with, fields, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

task_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name


class Items(Resource):
    @marshal_with(task_fields)
    def get(self):
        return Task.query.all()
    
    @marshal_with(task_fields)
    def post(self):
        parser.add_argument('name', type=str, help='name of todo')
        args = parser.parse_args(strict=True)
        task = Task(name=args['name'])
        db.session.add(task)
        db.session.commit()
        return task


class Item(Resource):
    @marshal_with(task_fields)
    def get(self, pk):
        return Task.query.filter_by(id=pk).first()

    @marshal_with(task_fields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        db.session.commit()
        return task
    
    @marshal_with(task_fields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks

api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>/')


if __name__ == '__main__':
    app.run(debug=True)
