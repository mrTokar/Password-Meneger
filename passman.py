from GUI import MainWindow, LoginWindow
from file_functions import check_directory


def main():
    log = LoginWindow()
    log.run()
    login = log.get_login()
    check_directory(login)
    window = MainWindow(login)
    window.start_show()
    window.run()


if __name__ == "__main__":
    main()
