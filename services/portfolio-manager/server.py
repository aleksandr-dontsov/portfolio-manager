from app import create_app

app = create_app()

if  __name__ == '__main__':
    # 127.0.0.1 is a default value.
    # Here we need to bind our service to the 0.0.0.0 
    # to make it accessible to machines other than docker.
    # Otherwise the service will be only accessible
    # from the docker localhost
    app.run(host="0.0.0.0", port=5000)