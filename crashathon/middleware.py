class CORSMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = ['GET', 'HEAD', 'OPTIONS']
        return response
