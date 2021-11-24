from datetime import datetime

class Comment():
    
    def __init__(self, id, post_id, author_id, content, created_on=None):
        self.id = id
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.created_on = created_on or datetime.now()