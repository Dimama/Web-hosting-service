from servers_service.app import app as app_servers

if __name__ == '__main__':
    app_servers.run(host='localhost', port=8082, debug=True)