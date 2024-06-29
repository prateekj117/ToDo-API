from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    """_summary_
    This renderer decides how to return user auth response.
    """
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({ 'errors' : data })
        else:
            response = json.dumps(data)
        return response
