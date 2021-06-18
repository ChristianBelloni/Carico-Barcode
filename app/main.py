from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import string

import pandas as pd

Base = declarative_base()

file = pd.read_excel(
    "spreadsheet/CODICI.xls", converters={'Codice Articolo': str, 'Codice Ean': str})
file = file.drop(axis=0, index=0)
file = file[["Codice Articolo", "Codice Ean", "Descrizione Articoli"]]
df = pd.DataFrame(file)


class Ordine(Base):
    __tablename__ = 'ordine'

    id = Column('id', Integer, primary_key=True)
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
    codice_interno = Column('codice_interno', String(20))
    descrizione = Column('descrizione', String(150))
    id_ordine = Column('id_ordine', Integer, ForeignKey('ordine.id'))
    n = Column('n', Integer)

    def __repr__(self):
        return f"<Articoli | {self.codice_ean} | {self.codice_interno} | {self.descrizione} | {self.n} | {self.id_ordine}>"


url = 'postgres://{0}:{1}@{2}:{3}/'.format(
    'postgres', '!Kkdfl123!', 'localhost', 5432)

engine = create_engine(url)
session_maker = sessionmaker(bind=engine)
session = session_maker()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def add_articoli(codice_ean, id_ordine, n, _session=None):
    session = session_maker() if not _session else _session
    articolo = session.query(Articolo).get(codice_ean)
    articoli = Articoli()
    articoli.codice_ean = codice_ean
    articoli.codice_interno = articolo.codice_interno
    articoli.descrizione = articolo.descrizione
    articoli.id_ordine = id_ordine
    articoli.n = n
    session.add(articoli)
    session.commit()
    if not _session:
        session.close()


def make_static_base():
    session = session_maker()

    for row in df.values:
        articolo = Articolo()
        articolo.codice_ean = row[1]
        articolo.codice_interno = row[0]
        articolo.descrizione = row[2]

        session.add(articolo)
    session.commit()
    session.close()


def read_ordine_from_csv(ordine_csv):
    #### read and format from xls file a dataframe of the order ####
    ordine_df = pd.read_excel(f"spreadsheet/{ordine_csv}.xls",
                              converters={'Codice Ean': str, "Quantita": int})
    ordine_df = ordine_df.drop(axis=0, index=0)
    ordine_df = ordine_df[["Codice Ean", "Quantita"]]
    ordine_df = pd.DataFrame(ordine_df)

    # make session, add ordine and append elements to ordine
    session = session_maker()
    ordine = Ordine()
    session.add(ordine)
    session.commit()
    for row in ordine_df.values:
        add_articoli(int(row[0]), ordine.id, row[1], _session=session)
    session.close()


def make_random_order(n_ordine, n_articoli):
    session = session_maker()
    for i in range(n_ordine):
        o = Ordine()
        chrs = (list("0123456789"))
        codice_list = random.choices(chrs, k=12)
        codice_ordine = ''
        for i in codice_list:
            codice_ordine += i
        o.codice_ordine = codice_ordine

        session.add(o)
        session.commit()
        query = session.query(Articolo).all()
        arts_in_ordine = random.sample(
            query, k=random.randint(n_articoli - 10, n_articoli + 10))
        for row in arts_in_ordine:
            add_articoli(
                int(row.codice_ean), o.id, random.randint(1, 70), _session=session)
    session.close()


make_static_base()
# read_ordine_from_csv("Ordine")
make_random_order(25, 16)
