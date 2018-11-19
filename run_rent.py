from rent_service.app import app as app_rent

if __name__ == '__main__':
    app_rent.run(host='localhost', port=8083, debug=True)