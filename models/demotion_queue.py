class Demotion_Queue():
  def __init__(self, id, action, admin_id, approver_one_id):
    self.id = id,
    self.action = action,
    self.admin_id = admin_id,
    self.approver_one_id = approver_one_id,
    self.admin = None
    self.approver_one = None
    