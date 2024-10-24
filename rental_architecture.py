from sqlalchemy import Enum, Column, Integer, DateTime, ForeignKey
from database import Base


# arquivo destinado a criação da tabela rental. sqlalchemy importa os datatypes enquanto o arquivo database.py importa o construtor da tabela "Base".

class Rental(Base):
    __tablename__ = 'rental'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_veiculo = Column(Integer, ForeignKey('vehicle.id'), nullable=False)
    data_alugar = Column(DateTime, nullable=False)
    data_previsao_retorno = Column(DateTime, nullable=False)
    status = Column(Enum('alugado', 'disponivel'), nullable=False)
