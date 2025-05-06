import subprocess

def run_command(command):
    print(f"Выполняется: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print("Ошибка при выполнении:", command)
        exit()

def main():
    version = input("Введите новую версию (например, v0.1.8): ").strip()

    run_command("git add .")
    run_command(f'git commit -m "Release {version}"')
    run_command(f"git tag {version}")
    run_command("git push origin main")
    run_command(f"git push origin {version}")

    print(f"✅ Версия {version} успешно отправлена на GitHub!")

if __name__ == "__main__":
    main()