# import typer
# from rich.tree import Tree
# import conda.exports
# import conda.api
# import os
# import json

# from .console import console


# def create_dep_graph(pkg, linked_data, color="green"):
#     # root_prefix = json.load(os.popen(f"conda info -e --json"))["root_prefix"]
#     # linked_data = conda.exports.linked_data(root_prefix)

#     root = Tree(f"[bold {color}]{pkg}")
#     for k in linked_data.keys():
#         if linked_data[k]["name"] == pkg.split(" ")[0]:
#             # check the dependencies
#             for deps in linked_data[k]["depends"]:
#                 # root.add(f"[magenta]{deps}")
#                 root.add(create_dep_graph(deps, linked_data, color="yellow"))

#     return root


# def show(
#     pkg_name: str = typer.Argument(
#         ..., help="Name of the package to show dependencies"
#     ),
# ):
#     root_prefix = json.load(os.popen(f"conda info -e --json"))["root_prefix"]
#     linked_data = conda.exports.linked_data(root_prefix)
#     console.print(create_dep_graph(pkg_name, linked_data))
