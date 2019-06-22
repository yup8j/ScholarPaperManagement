from backend.resources import *
from backend.handlers.InfoHandler import *
from flask_jwt_extended import jwt_required, get_jwt_identity



class GetInfo(API):
    @jwt_required
    def post(self):
        """

        :return:
        """
        ''' 用户鉴权：获得userid '''
        request.get_json(force=True)
        userid = get_jwt_identity()

        ''' 获取参数中的document_id '''
        parse = reqparse.RequestParser()
        parse.add_argument('document_id', type=str)
        args = parse.parse_args()
        document_id = args['document_id']

        ''' 调用handler获得metadata和topic '''
        docInfo, topic_list, topic_name = getInfo(userid, document_id)
        metadata = docInfo.metadata

        ''' 封装返回响应报文 '''
        author_list = ",".join(metadata.author)
        resp = jsonify({
            'title': metadata.title,
            'author': author_list,
            'year': metadata.publish_date,
            'source': metadata.publish_source,
            'paper_id': metadata.paper_id,
            'link': metadata.link_url,
            'topic': topic_list,
            'topic_name': topic_name
        })
        self.response = make_response(resp)
        self.response.status_code = 200
        return self.response


class EditInfo(API):
    @jwt_required
    def post(self):
        """
        """
        ''' 用户鉴权：获得userid '''
        userid = get_jwt_identity()

        req_json = request.get_json(force=True)
        editInfo(userid, req_json)
        self.response = {
            'status_code': 200,
            'msg': 'ok'
        }
        return self.response