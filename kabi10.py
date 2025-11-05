import os

def list_py_files():
    print("📂 Список всех файлов с расширением .py в репозитории:\n")

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(path)

if __name__ == "__main__":
    list_py_files()