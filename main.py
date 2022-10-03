from ast import arg
from asyncio import tasks

import json
from flask import Flask, jsonify,abort
from flask_restful import Resource, Api,reqparse

# instantiate flask app
app = Flask(__name__)
# De este modo se puede crear la api
api = Api(app)

#Cree datos fantasmas
todos={
  1:{"tasks":"Write Hello world Progrmas","summary":"write the code using python"},
  2:{"tasks":"Write Hello world Progrmas","summary":"write the code using python"},
  3:{"tasks":"Write Hello world Progrmas","summary":"write the code using python"},
  4:{"tasks":"Write Hello world Progrmas","summary":"write the code using python"}
}


# Definir un objeto para recibir un json
task_post_args=reqparse.RequestParser()
task_post_args.add_argument('task',type=str,help='Task is required',required=True)
task_post_args.add_argument('summary',type=str,help='Summary is required',required=True)

task_put_args=reqparse.RequestParser()
task_put_args.add_argument('task',type=str,help='Task is required',required=True)
task_put_args.add_argument('summary',type=str,help='Summary is required',required=True)

# Se maneja los metodos con clases que tienen las funciones http 
class ToDoList(Resource):
  def get(self):
    return todos
    # Http  para get es decir obtener
class ToDo(Resource):
  def get(self,todo_id):
    return todos[todo_id]
  
  def post(self,todo_id):
    args=task_post_args.parse_args()
    if todo_id in todos:
      abort(409,'Task ID already Token')
    todos[todo_id]={"task":args['task'],"summary":args['summary']}
    return jsonify(todos[todo_id])
  
  def put(self,todo_id):
    args =task_put_args.parse_args()
    if todo_id not in todos:
      abort(404,message="Task doesn't exist, cannot update")
    
    if args["task"]:
      todos[todo_id]["task"]=args["task"]
    if args["summary"]:
      todos[todo_id]["summary"]=args["task"]
    return todos[todo_id]
  

  def delete(self,todo_id):
    del todos[todo_id]
    return todos

api.add_resource(ToDo,'/todo/<int:todo_id>')
api.add_resource(ToDoList,'/todo')


if __name__ == '__main__':
   app.run(debug = True)