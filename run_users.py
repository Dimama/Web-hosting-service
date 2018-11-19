from users_service.app import app as app_users

if __name__ == '__main__':
    app_users.run(host='localhost', port=8081, debug=True)