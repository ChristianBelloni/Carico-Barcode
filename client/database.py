from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from PyQt5 import QtCore

Base = declarative_base()

url = 'postgres://{0}:{1}@{2}:{3}/postgres'.format('postgres',
                                                   '!Kkdfl123!', 'localhost', 5432)


class DatabaseThread(QtCore.QThread):
    progressEnded = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        o = get_orders()
        print(o)
        self.progressEnded.emit(o)


class Ordine(Base):
    __tablename__ = 'ordine'

    id = Column(Integer, primary_key=True)
    codice_ordine = Column('codice_ordine', String(15))
    articoli = relationship('Articoli', backref="ordine")


class Articolo(Base):
    __tablename__ = 'articolo'

    codice_ean = Column('codice_ean', BigInteger, primary_key=True)
    codice_interno = Column('codice_interno', String(20), unique=True)
    descrizione = Column('descrizione', String(150), unique=True)

    def __repr__(self):
        return f"<Articolo {self.codice_ean} {self.codice_interno} {self.descrizione}>"


class Articoli(Base):
    __tablename__ = 'articoli'

    id = Column('id', Integer, primary_key=True)
    codice_ean = Column('codice_ean', BigInteger)
    codice_interno = Column('codice_interno', String(20), unique=True)
    descrizione = Column('descrizione', String(150))
    id_ordine = Column('id_ordine', Integer, ForeignKey('ordine.id'))
    n = Column('n', Integer)

    def __repr__(self):
        return f"<Articoli | {self.codice_ean} | {self.codice_interno} | {self.descrizione} | {self.n} | {self.id_ordine}>"


engine = create_engine(url, echo=False)
session_factory = sessionmaker(bind=engine)


def get_orders():
    session = session_factory()

    query = session.query(Ordine).all()
    ret = [i for i in query]

    session.close()
    return ret


def get_articoli(id_ordine):
    session = session_factory()

    query = session.query(Ordine).get(id_ordine)
    ret = query.articoli

    session.close()
    return ret
