from click import command

from .utils import confirm, echo, error, fossil, prompt, run, run_pre_pos, select
from .Version import get_version


@command()
def branch():
    """
    Manipula los ramas convenientemente
    """

    current_branch = run(f"{fossil} branch current")
    version = get_version(current_branch)

    echo(f"Rama actual     {current_branch}")
    echo(f"Version actual  {version}")

    if run(f"{fossil} changes"):
        error("Existen cambios realice un commit primero")

    run_pre_pos("pre_branch", **locals())

    if current_branch == "trunk":
        version = version.next_version("patch")
        br_name = "hotfix-" + prompt("Escriba nombre de la rama")

        if confirm(f"Estas seguro de crear la rama {br_name}?"):
            run_pre_pos("pre_branch_trunk", **locals())

            run(f"{fossil} branch new {br_name} {current_branch}")
            run(f"{fossil} tag add v{str(version)} {br_name}")
            run(f"{fossil} update {br_name}")

            run_pre_pos("pos_branch_trunk", **locals())

    elif current_branch == "develop":
        branchs = [
            "feature: Una rama para agregar una caracteristica",
            "release: Una rama para arregrar el codigo antes de publicarlo",
            "cancelar: Cancelando la operacion",
        ]

        branch = select("Selecciona el tipo de rama a crear:", choices=branchs)

        if branch.startswith("cancelar"):
            error("Cancelando")

        if branch.startswith("feature"):
            br_name = "feature-" + prompt("Escriba nombre de la rama")
            version = version.next_version("minor").next_version("prerelease", "dev")
        else:
            br_name = f"release-{str(version)}"
            version = version.next_version("prerelease")

        if confirm(f"Estas seguro de crear la rama {br_name}?"):
            run_pre_pos("pre_branch_develop", **locals())

            run(f"{fossil} branch new {br_name} {current_branch}")
            run(f"{fossil} tag add v{str(version)} {br_name}")
            run(f"{fossil} update {br_name}")

            run_pre_pos("pos_branch_develop", **locals())

    elif current_branch.startswith("feature"):
        version = version.finalize_version()
        if confirm(f"Estas seguro de unificar la rama {current_branch} en develop?"):
            run_pre_pos("pre_branch_feature", **locals())

            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            if confirm("Deseas unificar la rama develop en trunk?"):
                run(f"{fossil} update trunk")
                run(f"{fossil} merge develop")
                run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
                run(f"{fossil} tag add v{str(version)} trunk")

                if confirm("Deseas regresar a la rama develop?"):
                    run(f"{fossil} update develop")

            run_pre_pos("pos_branch_feature", **locals())

    elif current_branch.startswith("release"):
        version = version.finalize_version()
        if confirm(f"Estas seguro de cerrar la version {version}?"):
            run_pre_pos("pre_branch_release", **locals())

            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            run(f"{fossil} update trunk")
            run(f"{fossil} merge develop")
            run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
            run(f"{fossil} tag add v{str(version)} trunk")

            if confirm("Deseas regresar a la rama develop?"):
                run(f"{fossil} update develop")

            run_pre_pos("pos_branch_release", **locals())

    elif current_branch.startswith("hotfix"):
        version = version.finalize_version()

        if confirm(f"Estas seguro de unificar la rama {current_branch} en develop?"):
            run_pre_pos("pre_branch_hotfix", **locals())

            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            if confirm("Deseas unificar la rama develop en trunk?"):
                run(f"{fossil} update trunk")
                run(f"{fossil} merge develop")
                run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
                run(f"{fossil} tag add v{str(version)} trunk")

                if confirm("Deseas regresar a la rama develop?"):
                    run(f"{fossil} update develop")

            run_pre_pos("pos_branch_hotfix", **locals())

    run_pre_pos("pos_branch", **locals())
