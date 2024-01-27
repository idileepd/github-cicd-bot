from db import DB,Account

new_user = Account(accountId='1', name='John Doe', gitToken="25")
DB.add(new_user)

print(DB.getItemByPk(Account, '1').name)