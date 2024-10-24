from sqlalchemy import Enum, Column, Integer, DateTime, ForeignKey
from main import Base

class Rental(Base):
    __tablename__ = 'rental'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_veiculo = Column(Integer, ForeignKey('vehicle.id'), nullable=False)
    data_alugar = Column(DateTime, nullable=False)
    data_retorno = Column(DateTime, nullable=True, default=None)
    data_previsao = Column(DateTime, nullable=False)
    status = Column(Enum('alugado','disponivel'), nullable=False)
