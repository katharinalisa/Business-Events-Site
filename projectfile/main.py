from website import create_app, create_database

if __name__ == '__main__':
    app = create_app()
    create_database(app)
    app.run()
