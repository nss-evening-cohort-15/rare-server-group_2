class Post_Tag():
    def __init__(self,id, post_id, tag_id):
        self.id = id,
        self.post_id = post_id,
        self.tag_id = tag_id,
        self.post = None,
        self.tag = None