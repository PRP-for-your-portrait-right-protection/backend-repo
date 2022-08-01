from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api
from db.db_connection import db_connection
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 용량제한
app.config.update(DEBUG=True)

CORS(app, resources={r'*': {'origins': '*'}})

db_connection(app)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

common_counter = metrics.counter(
    'flask_by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)
histogram = metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
    labels={'status': lambda r: r.status_code, 'path': lambda: request.path}
)

api = Api(
    app,
    version='v1',
    title="Silicon Project's API Server",
    description="PRP!",
    terms_url="/",
    contact="vivian0304@naver.com",
    license="MIT",
    prefix='/api/v1'
)
from namespaces import BlockCharacter, OriginVideo, ProccessedVideo, User, WhitelistFace
api.add_namespace(User.Users, '/users')
api.add_namespace(User.Auth, '/auth')
api.add_namespace(WhitelistFace.WhitelistFaces, '/whitelist-faces')
api.add_namespace(BlockCharacter.BlockCharacters, '/block-characters')
api.add_namespace(OriginVideo.OriginVideos, '/origin-videos')
api.add_namespace(ProccessedVideo.ProccessedVideos, '/processed-videos')

if __name__ == "__main__":
    app.run(port=5001, debug=True)
