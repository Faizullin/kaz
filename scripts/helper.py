import subprocess
import sys


def run_command(command):
    """Helper function to run a shell command."""
    try:
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: helper.py [dev|prod] [action] [additional_args]")
        sys.exit(1)

    # Get arguments
    env = sys.argv[1]
    action = sys.argv[2]
    additional_args = sys.argv[3:]  # Remaining arguments

    # Validate environment
    if env not in ["dev", "prod"]:
        print("Error: Environment must be 'dev' or 'prod'.")
        sys.exit(1)

    # Set compose file
    compose_file = f"../docker-compose.{env}.yml"

    container_name = "smart-shool-backend-1"
    settings_extension = "local" if env == "dev" else "prod"

    actions = ["build", "collectstatic", "migrate",
               "seed", "shell", "deploy", "run", "logs", "down", "remove_migrations_and_db"]
    if action not in actions:
        print(f"Error: Invalid action. Available actions: {','.join(actions)}")
        sys.exit(1)

    # Define actions
    if action == "build":
        print(f"Building for {env} environment...")
        run_command(f"docker-compose -f {compose_file} build")

    elif action == "collectstatic":
        print(f"Collecting static files for {env} environment...")
        run_command(
            f"docker exec -it {container_name} python3 manage.py collectstatic --noinput --settings=backend.settings.{settings_extension}")

    elif action == "migrate":
        print(f"Running migrations for {env} environment...")
        # run_command(
        #     f"docker exec -it {container_name} python3 manage.py makemigrations --settings=backend.settings.{settings_extension}")
        run_command(
            f"alembic upgrade head")

    elif action == "seed":
        print(f"Seeding database for {env} environment...")
        run_command(
            f"docker exec -it {container_name} python3 manage.py shell -c \"from seeding.seed import *;seed(False)\" --settings=backend.settings.{settings_extension}")

    elif action == "remove_migrations_and_db":
        print(f"Seeding database for {env} environment...")
        run_command(
            f"docker exec -it {container_name} python3 manage.py shell -c \"from seeding.remove_migrations_and_db import *;from seeding.seed import *;remove_migrations_and_db();seed(False)\" --settings=backend.settings.{settings_extension}")

    elif action == "shell":
        print(f"Opening shell for {env} environment...")
        run_command(f"docker exec -it {container_name} sh")

    elif action == "deploy":
        print(f"Deploying to {env} environment...")
        run_command(f"docker-compose -f {compose_file} down")
        run_command(f"docker-compose -f {compose_file} pull")
        run_command(f"docker-compose -f {compose_file} up -d --build")
        print("Deployment complete!")

    elif action == "run":
        print(f"Running to {env} environment...")
        run_command(f"docker-compose -f {compose_file} down")
        run_command(f"docker-compose -f {compose_file} up --build")
        print("Run complete!")

    elif action == "logs":
        print(f"Running to {env} environment...")
        run_command(f"docker-compose -f {compose_file} logs")

    elif action == "down":
        additional_args_str = " ".join(additional_args)
        print(f"Stopping containers...")
        run_command(f"docker-compose -f {compose_file} down {additional_args_str}")
        print("Containers stopped!")


if __name__ == "__main__":
    main()