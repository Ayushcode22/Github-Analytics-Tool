from sanic import Sanic
from Routes.routes import bp

app = Sanic(__name__)

app.blueprint(bp)



if __name__ == '__main__':
    app.run()