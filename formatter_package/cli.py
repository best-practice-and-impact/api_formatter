import ast
from copy import deepcopy
import typer
import json
from rich.prompt import Confirm, Prompt
from models import FileRecord
from models.user import User, Role
from services.session_manager import SessionManager
from services.uploader_service import UploaderService
from services.approval_service import ApprovalService
from services.export_service import ExportService
from services.db_service import DatabaseService
from rich import print as rprint
from rich.syntax import Syntax


app = typer.Typer()
db = DatabaseService()
uploader_service = UploaderService()
approval_service = ApprovalService()
export_service = ExportService()

def get_logged_in_user():
    session = SessionManager.load_session()
    if not session:
        typer.echo("[red]No active session. Please log in first.[/red]")
        raise typer.Exit()
    user = db.get_user(session["username"])
    if not user:
        typer.echo("[red]User not found.[/red]")
        raise typer.Exit()
    return user

def preview_and_edit_metadata(record: FileRecord):
    preview_copy = json.loads(json.dumps(deepcopy(record.metadata), default=str))
    json_preview = json.dumps(preview_copy, indent=2)
    syntax = Syntax(json_preview, "json", theme="monokai", line_numbers=True)
    rprint("\n[bold yellow]Metadata Preview:[/bold yellow]")
    rprint(syntax)

    # Ask if the user wants to edit metadata
    if Confirm.ask("\nDo you want to edit metadata now?"):
        updated_metadata = dict(record.metadata)
        for key in list(updated_metadata.keys()):
            current = updated_metadata[key]
            raw_input = Prompt.ask(f"{key} [{current}]", default=str(current))

            if isinstance(current, dict):
                try:
                    parsed = ast.literal_eval(raw_input)
                    if isinstance(parsed, dict):
                        new_val = parsed
                    else:
                        raise ValueError(f"Invalid input for {key}. Expected a dictionary.")
                except (ValueError, SyntaxError):
                    rprint(f"[red]Invalid input for {key}. Keeping current value.[/red]")
                    continue
            else:
                new_val = raw_input


            updated_metadata[key] = new_val
        rprint("\n[green]Metadata updated.[/green]")


        print(updated_metadata)

        rprint("\n[green]Metadata updated. Revalidating...[/green]")
        try:
            updated_data = uploader_service.edit_metadata(
                user=get_logged_in_user(),
                record=record,
                new_data=updated_metadata
            )
            record.metadata = updated_data
        except ValueError as e:
            rprint(f"[red]Validation failed: {e}[/red]")
            raise typer.Exit()

    return record

def handle_upload(file_path: str, is_edition: bool = False):
    user = get_logged_in_user()
    try:
        record = uploader_service.upload_edition(
            user=user,
            file_path=file_path
        ) if is_edition else uploader_service.upload_dataset(
            user=user,
            file_path=file_path
        )
    except Exception as e:
        typer.echo(f"[red]Upload failed: {e}[/red]")
        raise typer.Exit()

    # Preview and edit metadata
    record.metadata = preview_and_edit_metadata(record)

    # Ask if the user wants to save it
    if Confirm.ask("Save this upload to the database?"):
        db.add_file_record(record)
        typer.echo(f"[green]Saved: record ID {record.id} with status {record.status}[/green]")
    else:
        typer.echo("[yellow]Upload discarded. Run preview again when ready.[/yellow]")

@app.command()
def create_user(
        username: str = typer.Option(..., prompt=True, help="Username of the new user"),
        password: str = typer.Option(..., prompt=True,help="Password of the new user"),
        role: str = typer.Option(..., prompt=True, help="Role of the new user (uploader/approver)")
):
    role_enum = Role(role.lower())
    user = User(username=username, password=password, role=role_enum)
    db.add_user(user)
    typer.echo(f"User created: {username} as {role_enum.value}")


@app.command()
def login(
        username: str = typer.Option(..., prompt=True, help="Username of the user"),
        password: str = typer.Option(..., prompt=True, help="Password of the user")
):
    user = db.login(username, password)
    if not user:
        typer.echo("Invalid username or password.")
        raise typer.Exit()

    SessionManager.save_session(username=user.username, role=user.role.value)
    typer.echo(f"Logged in as {user.username} with role {user.role.value}")


@app.command()
def logout():
    SessionManager.clear_session()
    typer.echo("Logged out successfully.")


@app.command("upload")
def upload(file_path: str, is_edition: bool = False):
    if not file_path:
        file_path = Prompt.ask("File path", default="")

    if not file_path:
        typer.echo("[red]File path is required.[/red]")
        raise typer.Exit()

    if not file_path.endswith('.json'):
        typer.echo("[red]Invalid file type. Only .json.[/red]")
        raise typer.Exit()

    handle_upload(file_path, is_edition)


@app.command()
def preview(record_id: int):
    record = db.get_file_record(record_id)
    if not record:
        typer.echo("File not found.")
        raise typer.Exit()

    rprint(f"[bold green]Previewing Record ID: {record_id}[/bold green]\n")
    preview_and_edit_metadata(record)

@app.command()
def edit(record_id: int):
    user = get_logged_in_user()
    record = db.get_file_record(record_id)
    if not record:
        typer.echo("[red]File not found.[/red]")
        raise typer.Exit()

    record.metadata = preview_and_edit_metadata(record.metadata)

    # Ask if the user wants to save changes
    if Confirm.ask("Save updated metadata to database?"):
        db.update_file_record(record)
        typer.echo(f"[green]Record {record_id} updated successfully.[/green]")
    else:
        typer.echo("[yellow]Changes discarded.[/yellow]")


@app.command()
def approve(record_id: int):
    user = get_logged_in_user()
    record = db.get_file_record(record_id)
    if not record:
        typer.echo("Record not found.")
        raise typer.Exit()
    try:
        approval_service.approve(record, user)
        db.update_file_record(
            record=record
        )
        typer.echo(f"Record {record_id} approved by {user.username}")
    except Exception as e:
        typer.echo(f"Approval failed: {e}")

@app.command()
def export(
        record_id: int,
fmt: str = typer.Option("json", help="Format",
                        case_sensitive=False,
                        show_choices=True,
                        autocompletion=lambda: ["json", "yaml", "yml", "html"])

):
    user = get_logged_in_user()
    record = db.get_file_record(record_id)
    if not record:
        typer.echo("Record not found.")
        raise typer.Exit()

    fmt = fmt.lower()
    try:
        if fmt == "json":
            export_service.export_json(record)
        elif fmt in ["yaml", "yml"]:
            export_service.export_yaml(record)
        elif fmt == "html":
            path = f"data/output_{record_id}.html"
            export_service.export_html(record, path)
            typer.echo(f"Exported to {path}")
        else:
            typer.echo("Invalid format. Use json, yaml, or html.")
    except Exception as e:
        typer.echo(f"Export failed: {e}")


if __name__ == "__main__":
    app()



