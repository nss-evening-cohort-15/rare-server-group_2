
class Post_Reaction():
    
    def __init__(self, id, user_id, reaction_id, post_id):
        self.id = id
        self.user_id = user_id
        self.reaction_id = reaction_id
        self.post_id = post_id
        self.user = None
        self.reaction = None
        self.post = None

