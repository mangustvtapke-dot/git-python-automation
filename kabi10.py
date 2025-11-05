import subprocess

def get_changed_py_files():
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Ошибка при выполнении команды Git.")
        return
    
    print("Изменённые файлы с расширением .py:")
    lines = result.stdout.strip().split("\n")
    
    found = False
    for line in lines:
        if line and line.endswith(".py"):
            print(line)
            found = True
    
    if not found:
        print("✅ Нет изменённых файлов .py")

if __name__ == "__main__":
    get_changed_py_files()