#!/usr/bin/env python3
import os
import subprocess
import re


def generate_erd():
    """Generate the initial ERD using django-extensions."""
    print("Generating initial ERD...")
    exclude_models = "Session,AbstractBaseSession,LogEntry,ContentType,Permission,Group,PermissionsMixin,AbstractBaseUser,AbstractUser,UserManager"
    subprocess.run(
        [
            "python",
            "manage.py",
            "graph_models",
            "-a",
            "--exclude-models",
            f"{exclude_models}",
            "-o",
            "tmp/erd.dot",
        ]
    )


def customize_erd():
    """Customize the generated ERD."""
    print("Customizing ERD...")

    with open("tmp/erd.dot", "r") as f:
        content = f.read()

    # Add background color, white edges, and white edge labels
    content = content.replace(
        "digraph model_graph {",
        """digraph model_graph {
  bgcolor = "#44444c"
  edge [color = "white", fontcolor = "white"]""",
    )

    # Replace header background color
    content = content.replace('BGCOLOR="#1b563f"', 'BGCOLOR="#42a5f5"')

    # Replace any remaining Roboto fonts with Arial
    content = content.replace('FACE="Roboto"', 'FACE="Arial"')

    with open("tmp/erd.dot", "w") as f:
        f.write(content)


def render_image():
    """Render the final DOT file to PNG."""
    print("Rendering final image...")
    subprocess.run(["dot", "-Gdpi=300", "-Tpng", "tmp/erd.dot", "-o", "images/erd.png"])


def main():
    """Main function to generate the ERD."""
    try:
        generate_erd()
        customize_erd()
        render_image()
        print("ERD generation complete! Check images/erd.png")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
