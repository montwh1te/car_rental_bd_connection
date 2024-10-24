from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
from rental_architecture import Rental
from datetime import datetime, timedelta

DATABASE_URL ="mysql+mysqlconnector://root:@localhost/car_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Definição do modelo
class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    placa = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    valor_diaria = Column(Numeric(10, 2), nullable=False)


def insert_Vehicle(marca, modelo, placa, ano, valor_diaria):
    new_vehicle = Vehicle(marca=marca,  modelo=modelo, placa=placa, ano=ano, valor_diaria=valor_diaria)
    session.add(new_vehicle)
    session.commit()
    print(f'Veículo {marca} {modelo} adicionado com sucesso!')


def update_Vehicle(placa, new_marca, new_modelo, new_ano, new_valor_diaria):
    vehicle = session.query(Vehicle).filter_by(placa=placa).first()
    if vehicle:
        vehicle.marca = new_marca
        vehicle.modelo = new_modelo
        vehicle.ano = new_ano
        vehicle.valor_diaria = new_valor_diaria
        session.commit()
        print(f'Veículo com placa {placa} atualizado com sucesso.')
    else:
        print(f'Veículo com placa {placa} não encontrado.')


def delete_Vehicle(placa):
    vehicle = session.query(Vehicle).filter_by(placa=placa).first()
    if vehicle:
        session.delete(vehicle)
        session.commit()
        print(f'Veículo com placa {placa} deletado com sucesso.')
    else:
        print(f'Veículo com placa {placa} não encontrado.')


def list_Vehicles():
    all_vehicles = session.query(Vehicle).all()
    if all_vehicles:
        for vehicle in all_vehicles:
            print(f'ID: {vehicle.id}, Marca: {vehicle.marca}, Modelo: {vehicle.modelo}, Placa: {vehicle.placa}, Ano: {vehicle.ano}, Valor Diária: {vehicle.valor_diaria}')
    else:
        print('Nenhum veículo encontrado.')


def rental_Car():
    pass

def return_Car():
    pass


def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar veículo")
        print("2. Atualizar veículo")
        print("3. Deletar veículo")
        print("4. Listar veículos")
        print("5. Sair")

        choice = input("Opção: ")

        if choice == '1':
            marca = input("Marca do veículo: ")
            modelo = input("Modelo do veículo: ")
            placa = input("Placa do veículo: ")
            ano = int(input("Ano do veículo: "))
            valor_diaria = float(input("Valor da diária: "))
            insert_Vehicle(marca, modelo, placa, ano, valor_diaria)
        elif choice == '2':
            list_Vehicles()
            placa = input("Placa do veículo a ser atualizado: ")
            new_marca = input("Nova marca: ")
            new_modelo = input("Novo modelo: ")
            new_ano = int(input("Novo ano: "))
            new_valor_diaria = float(input("Novo valor da diária: "))
            update_Vehicle(placa, new_marca, new_modelo, new_ano, new_valor_diaria)
        elif choice == '3':
            list_Vehicles()
            placa = input("Placa do veículo a ser deletado: ")
            delete_Vehicle(placa)
        elif choice == '4':
            list_Vehicles()
        elif choice == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()
    session.close()

