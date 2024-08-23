
MAX_INIT_TRIES = 5

def is_main_page() -> bool:
    pass

def is_server_ok() -> bool:
    pass

def is_login_page() -> bool:
    pass

def login_procedure(driver,login:str,password:str) -> bool:
    pass

def reset_app(driver) -> None:
    pass

def initiqalize_app():#TODO add return type of driver
    pass

def change_server_procedure():
    pass

def main_procedure():
    counter = 10
    while counter < MAX_INIT_TRIES:
        if is_main_page():
            if is_server_ok():
                break
            else:
                change_server_procedure()
        else:
            if is_login_page():
                login_procedure()
            else:
                reset_app()
        counter+=1
    if is_main_page():
        return 'succes'
    else:
        print("Error while initializing")


if __name__ == "__main__":
    main_procedure()