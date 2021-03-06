import views

def routes(app):
    @app.route("/")
    def index(): return views.index() 

    @app.route("/register", methods=['POST'])
    def register_user(): return views.register_user()

    @app.route("/success")
    def new_user_page(): return views.new_user_page()

    @app.route("/wall")
    def access_wall(): return views.access_wall()

    @app.route("/login", methods=['POST'])
    def login(): return views.login()

    @app.route("/logout")
    def logout(): return views.logout()

    @app.route("/create", methods=['POST'])
    def create(): return views.create_message()
   
    @app.route("/delete/<id>")
    def delete(id): return views.delete_message(id)
    
    @app.route("/admin")
    def admin(): return views.access_admin()


