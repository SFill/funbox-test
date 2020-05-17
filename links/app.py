from flask import Flask, request, jsonify, json
from werkzeug.exceptions import HTTPException, BadRequest
from links.db import DomainsRepository
from marshmallow import ValidationError
from links.schema import VisitedLinksRequestShema, VisitedDomainsRequestShema
import time
repository = DomainsRepository()


def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "status": e.description,
    })
    response.content_type = "application/json"
    return response


def visited_links():
    ts = int(time.time())
    data = request.json
    try:
        validated_data = VisitedLinksRequestShema().load(data)
    except ValidationError:
        raise BadRequest(description='shema error')
    repository.add(
        ts,
        set(validated_data['links'])
    )
    return jsonify({'status': 'ok'})


def visited_domains():
    data = request.args
    try:
        validated_data = VisitedDomainsRequestShema().load(data)
    except ValidationError:
        raise BadRequest(description='shema error')
    from_ = validated_data['from_']
    to = validated_data['to']
    result = repository.get_range(from_, to)
    return jsonify({'domains': result, 'status': 'ok'})


def create_app():
    app = Flask(__name__)
    repository.init_app()
    app.add_url_rule('/visited_domains', 'visited_domains',
                     visited_domains, methods=['GET'])
    app.add_url_rule('/visited_links', 'visited_links',
                     visited_links, methods=['POST'])
    app.register_error_handler(HTTPException, handle_exception)

    return app
