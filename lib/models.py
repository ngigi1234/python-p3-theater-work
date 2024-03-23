from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///theaters.db')
Session = sessionmaker(bind=engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer(), primary_key=True)
    character_name = Column(String())
    
    auditions = relationship('Audition', backref=backref('role'))
    
    def __repr__(self):
        return f"<Role {self.character_name}>"
    
    def get_actors(self):
        return [audition.actor for audition in session.query(Audition).filter(Audition.role_id == self.id).all()]

    def set_actors(self):
        pass
    
    def get_locations(self):
        return [audition.location for audition in session.query(Audition).filter(Audition.role_id == self.id).all()]
    
    def set_locations(self):
        pass
    
    def lead(self):
        auditions = session.query(Audition).filter(Audition.role_id == self.id).all()
        
        for audition in auditions:
            if audition.hired:
                return audition
            
        return f"No actor has been hired for this role."
    
    def understudy(self):
        auditions = session.query(Audition).filter(Audition.role_id == self.id).all()
        
        if(len([audition for audition in auditions if audition.hired]) > 1):
            return [audition for audition in auditions if audition.hired][1]
                    
        return f"No actor has been hired for understudy for this role"
    
    actors = property(get_actors, set_actors)
    locations = property(get_locations, set_locations)
    
class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    
    role_id = Column(Integer(), ForeignKey('roles.id'))
    
    def __repr__(self):
        return f"Audition(id={self.id}, actor={self.actor}, location={self.location}, phone={self.phone}, hired={self.hired}, role_id={self.role_id})"
    
    def call_back(self):
        self.hired = True
        session.commit()
        
        return f"Hired status changed to true"