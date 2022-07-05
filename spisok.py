
def main():
    print('\n\n')
    url = input("Url?\n")
    resource_name = input("Название статьи?\n")
    
    data = "10.05.2022"

    result_string = f'\n{resource_name}: [Электронный ресурс] – URL: {url} (дата обращения {data})'
    return result_string


if __name__ == "__main__":
    while True:
        print(main())