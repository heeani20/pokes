from config import app
import controllers



#dashboard
app.add_url_rule('/', view_func=controllers.root, endpoint='root')
app.add_url_rule('/dashboard', view_func=controllers.dashboard, endpoint='dashboard')


#users
app.add_url_rule('/users/new', view_func=controllers.new_user, endpoint='users:new_user')
app.add_url_rule('/users/create', view_func=controllers.create_user, endpoint='users:create_user', methods=['POST'])
app.add_url_rule('/users/login', view_func=controllers.login, endpoint='users:login', methods=['POST'])
app.add_url_rule('/users/logout', view_func=controllers.logout, endpoint='users:logout')
app.add_url_rule('/users/<id>/poke', view_func=controllers.poke)
