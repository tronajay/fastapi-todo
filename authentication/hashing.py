from passlib.context import CryptContext
pwd = CryptContext(schemes =["bcrypt"],deprecated="auto")

class Hash():

   def bcrypt(password:str):
      ''' Encrypt/Hash the password using bycrypt'''
      return pwd.hash(password)

   def verify(hashed,normal):
      ''' Decrypt/Verify the password '''
      return pwd.verify(normal,hashed)