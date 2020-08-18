from app.api import bp

@bp.route('/news', methods=['GET'])
def get_all_news():
    return "Hello, World!"

@bp.route('/news/<string:search>', methods=['GET'])
def search_news(search):
    pass

@bp.route('/news', methods=['POST'])
def create_news():
    pass

@bp.route('/news/<int:id>', methods=['PATCH'])
def update_news(id):
    pass

@bp.route('/news', methods=['DELETE'])
def remove_news():
    pass
