from sqlalchemy import Column,CHAR,Integer,ForeignKey,create_engine,String,NVARCHAR,text
from sqlalchemy.orm import declarative_base,relationship,sessionmaker
import uvicorn
import router

Base = declarative_base()
engine = create_engine("sqlite:///test.db",echo=True,connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()


class Person(Base):
    __tablename__ = 'people'
    id = Column("id", Integer, primary_key=True)
    username = Column("username",String)
    email = Column("email",String,unique=True)
    password = Column("password",NVARCHAR(100))
    items = relationship("Item",back_populates="owner")

    def __repr__(self):
        return f'({self.id}. {self.username} | {self.email} | {self.password})';


class Item(Base):
    __tablename__ = 'items'
    id = Column("id",Integer,primary_key=True)
    name = Column("name",String)
    person_id = Column("person_id",Integer,ForeignKey("people.id"))
    owner = relationship("Person",back_populates="items")

    def __repr__(self):
        return f'{self.id}. {self.name} owner_is : {self.owner}'
# p = Person(username="rith",email="rith@gmail.com",password="rithtest")
# session.add(p)
# session.commit()


# i1 = Item(name="pizza",person_id=1)
# i2 = Item(name="burger",person_id=1)
# session.add_all([i1,i2])
# session.commit()

# person = session.query(Person).filter(Person.id == 1).first()
# results = session.query(Person,Item).filter(Person.id == 1,Item.person_id == 1).all()
# print(results)


# Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run("main:router.app",reload=True)
