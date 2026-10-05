import git
import os

try:
    # Abre el repositorio en el directorio de trabajo actual
    repo = git.Repo("./", search_parent_directories=True)
    
    print(f" Repositorio detectado en: {repo.working_dir}")
    print(f" Rama actual: {repo.active_branch.name}")
    
    # Intenta obtener el último commit si existe
    ultimo_commit = repo.head.commit
    print("\n Último commit local:")
    print(f"  • Hash: {ultimo_commit.hexsha[:7]}")
    print(f"  • Autor: {ultimo_commit.author.name}")
    print(f"  • Mensaje: {ultimo_commit.message.strip()}")
    
    lista_tags = list(repo.tags)
    
    if lista_tags:
        ultimos_tags = [tag.name for tag in lista_tags]
        print(f"\n Últimas releases detectadas: {ultimos_tags}")
    else:
        print("\n No se encontraron tags/releases locales.")

except git.exc.InvalidGitRepositoryError:
    print(f" Error: La carpeta '{os.getcwd()}' no es un repositorio de Git válido.")
except TypeError:
    # Capturamos el TypeError estándar de Python por si el repo está vacío
    print(" El repositorio está vacío (no tiene commits todavía).")