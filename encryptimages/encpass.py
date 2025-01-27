import keyring 

service_id = 'PYTHON_SHIT'

def main() -> None: 
    keyring.set_password(service_id, 'alberto', 'mypassword')
    x = keyring.get_credential(service_id, 'alberto')
    print(x.password)
    keyring.set_keyring()
    

if __name__ == "__main__": main()