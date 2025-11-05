import subprocess
import datetime
import os

class GitAutomation:
    def __init__(self):

        if not os.path.exists(".git"):
            print("❌ Репозиторий не найден. Инициализация нового...")
            self.run_command(["git", "init"])
        else:
            print("✅ Git-репозиторий найден.")

    def run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"⚠ Ошибка при выполнении команды: {' '.join(command)}")
            print(e.stderr)
            return None

    def get_changed_files(self):
        result = self.run_command(["git", "status", "--porcelain"])
        if not result:
            return []
        changed_files = [line[3:] for line in result.splitlines()]
        return changed_files

    def save_changed_files(self, filename="kabi.txt"):
        changed_files = self.get_changed_files()
        if changed_files:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Изменённые файлы:\n")
                f.write("\n".join(changed_files))
            print(f"📄 Список изменённых файлов сохранён в {filename}")
        else:
            print("✅ Нет изменённых файлов для записи.")
            print(f"📂 Текущая директория: {os.getcwd()}")


    def commit_changes(self, message="Auto commit"):
        self.save_changed_files("kabi.txt")

        self.run_command(["git", "add", "."])
        print("🟢 Все файлы добавлены в индекс.")

        commit_message = f"{message} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        self.run_command(["git", "commit", "-m", commit_message])
        print(f"✅ Коммит выполнен: {commit_message}")

        self.run_command(["git", "push"])
        print("🚀 Изменения отправлены на сервер (если настроен remote).")


if __name__ == "__main__":
    git_auto = GitAutomation()
    git_auto.commit_changes("Автоматический коммит с kabi.txt")