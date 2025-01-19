from django.core.management.base import BaseCommand
import os
import autopep8


class Command(BaseCommand):
    help = 'Lint Python files in the project'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.exclude_paths = ["venv", ".git", ]

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='?',
            default='',
            help='Specify a path to a folder or file to lint'
        )
        parser.add_argument(
            '--exclude',
            nargs='+',
            default=[],
            help='Specify folders or files to exclude from linting'
        )

    def handle(self, *args, **options):
        path = options['path']
        self.exclude_paths += options['exclude']

        if not path:
            self.stdout.write(self.style.NOTICE(
                'No path provided. Linting the entire project...'))
            self.lint_project(self.exclude_paths)
        elif os.path.isfile(path):
            self.stdout.write(self.style.NOTICE(f'Linting file: {path}...'))
            self.lint_file(path)
        elif os.path.isdir(path):
            self.stdout.write(self.style.NOTICE(f'Linting folder: {path}...'))
            self.lint_folder(path, self.exclude_paths)
        else:
            self.stdout.write(self.style.ERROR(f'Invalid path: {path}'))

        self.stdout.write(self.style.SUCCESS('Linting complete!'))

    def lint_project(self, exclude_paths):
        PROJECT_ROOT = os.getcwd()
        self.lint_folder(PROJECT_ROOT, exclude_paths)

    def lint_folder(self, folder_path, exclude_paths):
        for root, dirs, files in os.walk(folder_path):
            # Exclude specified folders
            dirs[:] = [d for d in dirs if d not in exclude_paths]
            if 'migrations' in dirs:
                dirs.remove('migrations')

            for file in files:
                if file.endswith('.py') and file not in exclude_paths:
                    file_path = os.path.join(root, file)
                    self.lint_file(file_path)

    def lint_file(self, file_path):
        with open(file_path, 'r+') as file:
            code = file.read()
            formatted_code = autopep8.fix_code(code)
            file.seek(0)
            file.write(formatted_code)
            file.truncate()
