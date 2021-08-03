from GUI import MainWindow
from file_functions import check_directory


def main():
    check_directory()
    window = MainWindow(620,610)
    window.start_show()
    window.run()


if __name__ == "__main__":
    main()
