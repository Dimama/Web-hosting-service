from gateway_service.app import app as app_gateway

if __name__ == '__main__':
    app_gateway.run(host='localhost', port=8080, debug=True)