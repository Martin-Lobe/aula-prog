from app import app, db

if __name__ == "__main__":
    db.create_all()
    # Criação das tabelas no arquivo do BD
    app.run(debug=True)
    # Execução da aplicação com a depuração para verificar erros

'''
*Depuração (em inglês: debugging, debug)
é o processo de encontrar e reduzir defeitos 
num aplicativo de software ou mesmo em hardware.
'''
