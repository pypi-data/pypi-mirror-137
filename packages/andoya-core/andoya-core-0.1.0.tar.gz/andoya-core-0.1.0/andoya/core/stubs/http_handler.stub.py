from apig_wsgi import make_lambda_handler
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

handle = make_lambda_handler(app)
