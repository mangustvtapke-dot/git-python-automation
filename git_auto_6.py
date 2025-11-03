#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git автоматтандыру скрипті - 6-шы нұсқа
Ерекшелігі: Commit жасалған соң, нәтижені log.txt файлына жазу
"""

import subprocess
import os
from datetime import datetime


def run_git_command(command):
    """
    Git командасын орындау және нәтижені қайтару
    
    Args:
        command (list): Git командасы list форматында
    
    Returns:
        tuple: (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def write_to_log(message):
    """
    log.txt файлына мәліметтерді жазу
    
    Args:
        message (str): Жазылатын хабарлама
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"✓ Log файлына жазылды: {message}")
    except Exception as e:
        print(f"✗ Log файлына жазу қатесі: {e}")


def git_status():
    """Git статусын тексеру"""
    print("\n=== Git статусы ===")
    code, out, err = run_git_command(["git", "status", "--short"])
    
    if code == 0:
        if out.strip():
            print("Өзгерістер табылды:")
            print(out)
            return True
        else:
            print("Өзгерістер жоқ")
            return False
    else:
        print(f"✗ Қате: {err}")
        return False


def git_add(files="."):
    """
    Файлдарды staging area-ға қосу
    
    Args:
        files (str): Қосылатын файлдар (әдепкі: барлық файлдар)
    """
    print(f"\n=== Git add: {files} ===")
    code, out, err = run_git_command(["git", "add", files])
    
    if code == 0:
        print("✓ Файлдар сәтті қосылды")
        write_to_log(f"git add {files} - СӘТТІ")
        return True
    else:
        print(f"✗ Қате: {err}")
        write_to_log(f"git add {files} - ҚАТЕ: {err}")
        return False


def git_commit(message):
    """
    Commit жасау және нәтижені log.txt-ке жазу
    
    Args:
        message (str): Commit хабарламасы
    """
    print(f"\n=== Git commit: {message} ===")
    code, out, err = run_git_command(["git", "commit", "-m", message])
    
    if code == 0:
        print("✓ Commit сәтті жасалды")
        
        # Соңғы commit туралы мәліметті алу
        code2, commit_info, _ = run_git_command([
            "git", "log", "-1", "--format=%H %s - %an (%ad)"
        ])
        
        if code2 == 0:
            commit_details = commit_info.strip()
            log_message = f"COMMIT ЖАСАЛДЫ: {commit_details}"
            write_to_log(log_message)
            
            # Қосымша: commit санын есептеу
            code3, commit_count, _ = run_git_command([
                "git", "rev-list", "--count", "HEAD"
            ])
            if code3 == 0:
                count = commit_count.strip()
                write_to_log(f"Жалпы commit саны: {count}")
        
        return True
    else:
        error_msg = err if err else out
        print(f"✗ Қате: {error_msg}")
        write_to_log(f"COMMIT ҚАТЕСІ: {error_msg}")
        return False


def git_push(remote="origin", branch="main"):
    """
    Өзгерістерді remote repository-ге жіберу
    
    Args:
        remote (str): Remote аты (әдепкі: origin)
        branch (str): Branch аты (әдепкі: main)
    """
    print(f"\n=== Git push: {remote} {branch} ===")
    code, out, err = run_git_command(["git", "push", remote, branch])
    
    if code == 0:
        print("✓ Push сәтті орындалды")
        write_to_log(f"git push {remote} {branch} - СӘТТІ")
        return True
    else:
        error_msg = err if err else out
        print(f"✗ Қате: {error_msg}")
        write_to_log(f"git push {remote} {branch} - ҚАТЕ: {error_msg}")
        return False


def git_log_summary():
    """Git log қысқаша ақпаратын көрсету және log.txt-ке жазу"""
    print("\n=== Соңғы 5 commit ===")
    code, out, err = run_git_command([
        "git", "log", "-5", "--oneline", "--decorate"
    ])
    
    if code == 0:
        print(out)
        write_to_log("GIT LOG қаралды (соңғы 5 commit)")
        return True
    else:
        print(f"✗ Қате: {err}")
        return False


def main():
    """Негізгі функция"""
    print("=" * 60)
    print("Git автоматтандыру - 6-шы нұсқа")
    print("Ерекшелігі: Commit нәтижесін log.txt файлына жазу")
    print("=" * 60)
    
    # Log файлын бастау
    write_to_log("=" * 50)
    write_to_log("GIT АВТОМАТТАНДЫРУ БАСТАЛДЫ")
    
    # 1. Статусты тексеру
    if not git_status():
        write_to_log("Өзгерістер табылмады, скрипт аяқталды")
        return
    
    # 2. Файлдарды қосу
    if not git_add():
        return
    
    # 3. Commit хабарламасын енгізу
    commit_msg = input("\nCommit хабарламасын енгізіңіз: ").strip()
    if not commit_msg:
        commit_msg = f"Auto commit - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # 4. Commit жасау (нәтиже log.txt-ке автоматты жазылады)
    if not git_commit(commit_msg):
        return
    
    # 5. Log-ты көрсету
    git_log_summary()
    
    # 6. Push жасау (опция)
    do_push = input("\nRemote-ке push жасау керек пе? (y/n): ").strip().lower()
    if do_push == 'y':
        git_push()
    
    write_to_log("GIT АВТОМАТТАНДЫРУ АЯҚТАЛДЫ")
    write_to_log("=" * 50)
    print("\n✓ Барлық операциялар аяқталды!")
    print("✓ Нәтижелер log.txt файлында сақталды")


if __name__ == "__main__":
    # Git repository-де екенін тексеру
    if not os.path.exists(".git"):
        print("✗ Қате: Бұл Git repository емес!")
        print("Алдымен 'git init' командасын орындаңыз")
    else:
        main()