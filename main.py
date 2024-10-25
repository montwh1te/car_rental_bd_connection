from database import session, Base, engine
from sqlalchemy import Column, Integer, String, Numeric, Enum
from rental_architecture import Rental
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound


# Definição do modelo
class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    placa = Column(String(50), nullable=False, unique=True)
    ano = Column(Integer, nullable=False)
    valor_diaria = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum('alugado', 'disponivel'), default='disponivel', nullable=False)


# inserção de um veículo na tabela Vehicle do banco de dados
def insert_Vehicle(marca, modelo, placa, ano, valor_diaria):
    new_vehicle = Vehicle(marca=marca.lower(), modelo=modelo.lower(), placa=placa.upper(), ano=ano,
                          valor_diaria=valor_diaria)
    session.add(new_vehicle)
    session.commit()
    print(f'Veículo {marca} {modelo} adicionado com sucesso!')


# atualização de um veículo na tabela Vehicle do banco de dados
def update_Vehicle(placa, new_marca, new_modelo, new_ano, new_valor_diaria):
    vehicle = session.query(Vehicle).filter_by(placa=placa.upper()).first()
    if vehicle:
        vehicle.marca = new_marca.lower()
        vehicle.modelo = new_modelo.lower()
        vehicle.ano = new_ano
        vehicle.valor_diaria = new_valor_diaria
        session.commit()
        print(f'Veículo com placa {placa} atualizado com sucesso.')
    else:
        print(f'Veículo com placa {placa} não encontrado.')


# deleção de um veículo na tabela Vehicle do banco de dados
def delete_Vehicle(placa):
    vehicle = session.query(Vehicle).filter_by(placa=placa.upper()).first()
    if vehicle:
        session.delete(vehicle)
        session.commit()
        print(f'Veículo com placa {placa} deletado com sucesso.')
    else:
        print(f'Veículo com placa {placa} não encontrado.')


# lista dos veículos na tabela Vehicle do banco de dados
def list_Vehicles():
    all_vehicles = session.query(Vehicle).all()
    if all_vehicles:
        for vehicle in all_vehicles:
            print(
                f'ID: {vehicle.id}, Marca: {vehicle.marca}, Modelo: {vehicle.modelo}, Placa: {vehicle.placa}, Ano: {vehicle.ano}, Valor Diária: {vehicle.valor_diaria}, Status:{vehicle.status}')
    else:
        print('Nenhum veículo encontrado.')


# ação que atribui um determinado carro a um aluguel
def rental_Car(data_alugar, placa_carro):
    # query pela placa
    carro_selecionado = session.query(Vehicle).filter_by(placa=placa_carro.upper()).first()
    id_veiculo = carro_selecionado.id

    # verificação se a query foi realizada corretamente e se o veículo existe.
    if not carro_selecionado:
        print(f'Veículo com placa {placa_carro} não encontrado.')
        return

    # verificação se o veículo já foi alocado.
    try:
        session.query(Vehicle).filter_by(placa=placa_carro.upper(), status='alugado').one()
        print('Este veículo já está alugado!')
        return
    except NoResultFound:
        # nenhum locação encontrada, continuar...
        pass

    # verificação da variável "data_alugar" em formato datetime para operação da previsão de entrega.
    if isinstance(data_alugar, str):
        data_alugar = datetime.strptime(data_alugar, '%d/%m/%Y')
    previsao_entrega = data_alugar + timedelta(days=3)

    # instanciando o novo aluguel
    new_rental = Rental(data_previsao_retorno=previsao_entrega, data_alugar=data_alugar, id_veiculo=id_veiculo)
    carro_selecionado.status = 'alugado'

    # adicionando novo aluguel ao database
    if new_rental:
        session.add(new_rental)
        session.commit()
        print(f'O {carro_selecionado.marca} {carro_selecionado.modelo} foi alugado com sucesso!')


# ação que atribui um determinado carro a uma devolução de um aluguel
def return_Car(data_devolucao, placa_carro):
    carro_selecionado = session.query(Vehicle).filter_by(placa=placa_carro.upper()).first()
    id_veiculo = carro_selecionado.id

    # verificação se a query foi realizada corretamente e se o veículo existe.
    if not carro_selecionado:
        print(f'Veículo com placa {placa_carro} não encontrado.')
        return

    # verificação se o veículo já foi devolvido.
    locacao_existente = session.query(Rental).filter_by(id_veiculo=id_veiculo, data_retorno=None).first()
    if not locacao_existente:
        print('Este veículo já foi devolvido!')
        return

    # filtro na tabela Rental para obter informações das datas
    stats_aluguel = session.query(Rental).filter_by(id_veiculo=carro_selecionado.id, data_retorno=None).first()

    # verificação de type: str para type: datetime, para que a operação de diferença de data seja bem sucedida
    data_retorno = stats_aluguel.data_previsao_retorno
    if isinstance(data_devolucao, str):
        data_devolucao = datetime.strptime(data_devolucao, '%d/%m/%Y')

    # operação de diferença de data, se diferença menor que 0, então veículo foi entregue dentro do prazo, caso contrário, será informado em quantos dias a devolução foi atrasada.
    diff_data_aluguel = data_devolucao - data_retorno
    if diff_data_aluguel.days <= 0:
        print('Veículo entregue dentro do prazo!')
    else:
        print(f'A sua entrega atrasou {diff_data_aluguel.days} dias.')

    locacao_existente.data_retorno = data_devolucao
    locacao_existente.dias_atrasados = diff_data_aluguel.days
    carro_selecionado.status = 'disponivel'
    session.commit()


def filter_Menu():
    print("\nEscolha uma opção:")
    print("1. Por marca")
    print("2. Por disponibilidade")
    selected_filter = str(input('Opção: '))
    try:
        if selected_filter == '1':
            brand_Filter()
        elif selected_filter == '2':
            disponibility_Filter()
    except:
        print('Informe um número do filtro de pesquisa válido:')


def brand_Filter():
    brand_selected = str(input('Digite o nome da marca que deseja buscar: '))
    selected_cars = session.query(Vehicle).filter_by(marca=brand_selected.lower()).all()
    for car in selected_cars:
        print(
            f'ID: {car.id}, Modelo: {car.modelo}, Placa: {car.placa}, Ano: {car.ano}, Valor Diária: {car.valor_diaria}')


def disponibility_Filter():
    disponibles_cars = session.query(Vehicle).filter_by(status='disponivel').all()
    print('-' * 20)
    for car in disponibles_cars:
        print(
            f'Marca: {car.marca}, Modelo: {car.modelo}, Placa: {car.placa}, Ano: {car.ano}, Valor Diária: {car.valor_diaria}')
    print('-' * 20)


def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar veículo")
        print("2. Atualizar veículo")
        print("3. Deletar veículo")
        print("4. Listar veículos")
        print("5. Alugar veículo")
        print("6. Devolver veículo")
        print("7. Filtro de busca")
        print("8. Sair")

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
            list_Vehicles()
            placa_carro = str(input('Placa do veículo que será alugado: '))
            data_alugar = str(input('Data em que o veículo será alugado (d/m/y): '))
            rental_Car(data_alugar, placa_carro)
        elif choice == '6':
            list_Vehicles()
            placa_carro = str(input('Placa do veículo que será devolvido: '))
            data_dev = str(input('Data em que o veículo será devolvido (d/m/y): '))
            return_Car(data_dev, placa_carro)
        elif choice == '7':
            filter_Menu()
        elif choice == '8':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)  # cria-se a engine do bd
    main()  # chama o menu principal
    session.close()  # fecha a sessão do bd enquanto o programa não está em execução
