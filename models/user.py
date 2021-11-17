from datetime import datetime

class User():
  def __init__(self, first_name, last_name, email, 
               password='', bio='', username='', profile_image_url='', 
               created_on=None, active=False, id=None):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.bio = bio
    self.username = username #Can also set username as email: self.username = email; otherwise create another username field
    self.profile_image_url = profile_image_url
    self.created_on = created_on or datetime.now() #When the 1st one is false, run the 2nd one ; only run 1st when true
    self.active = active
  