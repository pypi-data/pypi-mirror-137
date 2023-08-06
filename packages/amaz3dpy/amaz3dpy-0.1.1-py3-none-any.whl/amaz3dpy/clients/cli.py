import json
import sys, re, os, timeago
from appdirs import *
from amaz3dpy.clients import Amaz3DClient

from cmd import Cmd
from pyfiglet import Figlet
from InquirerPy import prompt
from clint.textui import colored
from columnar import columnar
from click import style
from dateutil import parser
from datetime import datetime, timezone
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator


from amaz3dpy.models import OptimizationOutputFormat, OptimizationParams, OptimizationPreset

class Cli(Cmd):

    @property
    def prompt(self):
        return '(amaz3d) '

    def __init__(self):
        super().__init__()

        try:
            endpoint_info = json.load(open(self.__get_endpoint_path()))
        except:
            endpoint_info = {}

        self._amaz3dclient = Amaz3DClient(**endpoint_info)
        f = Figlet(font='slant')
        self.intro = f.renderText('AMAZ3D') + "\nPowered By Adapta Studio\nType help or ? to list commands.\n"

    def do_exit(self, arg):
        '''Exit from AMAZ3D'''
        self._amaz3dclient.close()
        print('Thank you for using AMAZ3D')
        sys.exit()

    def do_clear_configurations(self, arg):
        '''Clear configurations'''
        questions = [
            {
                "type": "confirm",
                "message": "Do you want to clear all configurations:",
                "name": "confirm",
                "default": False,
            },
        ]

        result = prompt(questions)

        if result["confirm"]:
            self._amaz3dclient.clear_configs()

            try:
                os.remove(self.__get_endpoint_path())
            except:
                pass
            
            print(colored.green("Please restart to apply changes"))

    def __get_endpoint_path(self):
        appname = "amaz3dpy"
        appauthor = "Adapta Studio"
        app_path = user_data_dir(appname, appauthor)
        return os.path.join(app_path, "endpoint.json")

    def do_change_endpoint(self, arg):
        '''Change endpoint'''
        questions = [
            {
                "type": "input", 
                "message": "Endpoint:", 
                "default": "amaz3d_backend.adapta.studio",
                "name": "url",
            },
            {
                "type": "confirm",
                "message": "Use SSL:",
                "name": "use_ssl",
                "default": True,
            },
        ]

        result = prompt(questions)
        json.dump(result, open(self.__get_endpoint_path(), 'w'))
        print(colored.green("Endpoint changed successfully. Please restart to apply changes"))

    def do_login(self, arg):
        '''Perform login'''
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        questions = [
            {
                "type": "input", 
                "message": "Email:", 
                "name": "email",
                "validate": lambda result: re.fullmatch(email_regex, result),
                "invalid_message": "Invalid email address",
            },
            {
                "type": "password",
                "message": "Password:",
                "name": "password",
                "transformer": lambda _: "[hidden]",
            },
            {
                "type": "confirm",
                "message": "Keep me logged in",
                "name": "keep_the_user_logged_in",
                "default": True,
            },
        ]
        result = prompt(questions)
        login_result = self._amaz3dclient.login(**result) 
        if login_result:
            print(colored.green("Log in succeeded"))
        else:
            print(colored.red("Unable to login"))

    def do_logout(self, arg):
        '''Perform logout'''
        questions = [
            {
                "type": "confirm",
                "message": "Are you sure you want to log out?",
                "name": "logout",
                "default": False,
            },
        ]

        result = prompt(questions)

        if result["logout"]:
            self._amaz3dclient.logout()
            print(colored.green("Log out succeeded"))

    def do_load_projects(self, arg):
        '''Load projects'''
        num = self._amaz3dclient.load_projects()
        if num:
            print(colored.green("Projects loaded: {0}".format(num)))
        else:
            print(colored.yellow("No projects loaded"))

    def do_projects(self, arg):
        '''View loaded projects'''
        now = datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        data = []

        for np in self._amaz3dclient.new_projects():
            data.append([
                f"{style(np.id, fg='yellow')}",
                np.name, 
                np.conversionStatus,
                np.objectModel.triangleCount if np.objectModel else "", 
                np.objectModel.fileSizeBytes if np.objectModel else "", 
                np.optimizationsCount if np.optimizationsCount is not None else 0, 
                timeago.format(parser.parse(np.lastActivityAt), now) if np.lastActivityAt is not None else ""
            ])

        for np in self._amaz3dclient.projects():
            data.append([
                f"{style(np.id, fg='blue')}", 
                np.name, 
                np.conversionStatus,
                np.objectModel.triangleCount, 
                np.objectModel.fileSizeBytes, 
                np.optimizationsCount if np.optimizationsCount is not None else 0, 
                timeago.format(parser.parse(np.lastActivityAt), now) if np.lastActivityAt is not None else ""
            ])

        if(len(data) == 0):
            print(colored.yellow("No projects available"))
            return

        table = columnar(data, headers=['Id', 'Name', 'Status', 'Triangles', 'Size', 'Exports created', 'Last Activity'], no_borders=True)
        print(table)

    def do_create_project(self, arg):
        '''Create a projects'''
        home_path = "~/" if os.name == "posix" else "C:\\"

        def file_validator(result) -> bool:
            return os.path.isfile(os.path.expanduser(result)) and result.lower().endswith(('.obj', '.fbx', '.stl', '.3ds'))

        questions = [
            {
                "type": "input",
                "message": "Project name",
                "name": "name",
                "validate": lambda result: len(result) > 3,
            },
            {
                "type": "filepath",
                "message": "Object",
                "name": "file_path",
                "default": home_path,
                "validate": file_validator,
            },
        ]

        result = prompt(questions)
        res = self._amaz3dclient.create_project(**result)
        print(colored.green("Project {0} created successfully".format(res.id)))

    def do_select_project(self, arg):
        '''Select a projects'''
        questions = [
            {
                "type": "input",
                "message": "Project id",
                "name": "id",
            },
        ]

        result = prompt(questions)

        try:
            self._amaz3dclient.select_a_project(**result)
            print(colored.green("Project {0} selected".format(result["id"])))
        except ValueError as ex:
            print(colored.red(ex))

    def do_delete_selected_project(self, arg):
        '''Delete the selected project'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [
            {
                "type": "confirm",
                "message": "Are you sure you want to delete project {}?".format(project.id),
                "name": "confirm",
                "default": False,
            },
        ]

        result = prompt(questions)

        if not result['confirm']:
            return

        try:
            self._amaz3dclient.delete_selected_project()
            print(colored.green("Project {0} deleted successfully".format(project.id)))
        except ValueError as ex:
            print(colored.red(ex))

    def do_load_optimizations(self, arg):
        '''Load optimizations'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        num = self._amaz3dclient.load_optimizations()
        if num:
            print(colored.green("Optimizations for {1} loaded: {0}".format(num, project.id)))
        else:
            print(colored.yellow("No optimizations loaded for {0}".format(project.id)))

    def do_optimizations(self, arg):
        '''View optimizations'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        now = datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc)
        data = []

        def format_parameters(parameters):
            return "Face reduction {0}\nFeature Importance {1}\nPreserve Boundary Edges {2}\nPreserve Hard Edges {3}\nPreserve Smooth Edges {4}\nRetexture {5}\nMerge Duplicated UV {6}\nRemove Isolated Vertices {7}\nRemove Non Manifold Faces {8}\nRemove Duplicated Faces {9}\nRemove Duplicated Boundary Vertices {10}\nRemove Degenerate Faces {11}".format(
                    parameters.face_reduction,
                    parameters.feature_importance,
                    "Yes" if parameters.preserve_boundary_edges else "No",
                    "Yes" if parameters.preserve_hard_edges else "No",
                    "Yes" if parameters.preserve_smooth_edges else "No",
                    "Yes" if parameters.retexture else "No",
                    "Yes" if parameters.merge_duplicated_uv else "No",
                    "Yes" if parameters.remove_isolated_vertices else "No",
                    "Yes" if parameters.remove_non_manifold_faces else "No",
                    "Yes" if parameters.remove_duplicated_faces else "No",
                    "Yes" if parameters.remove_duplicated_boundary_vertices else "No",
                    "Yes" if parameters.remove_degenerate_faces else "No",
                )

        for no in self._amaz3dclient.new_optimizations():
            data.append([
                f"{style(no.id, fg='yellow')}",
                no.name, 
                no.status,
                no.preset,
                None, 
                timeago.format(parser.parse(no.lastActivityAt), now) if no.lastActivityAt is not None else ""
            ])

        for no in self._amaz3dclient.optimizations():
            data.append([
                f"{style(no.id, fg='blue')}", 
                no.name, 
                no.status,
                no.preset,
                format_parameters(no.params) if no.params else "", 
                timeago.format(parser.parse(no.lastActivityAt), now) if no.lastActivityAt is not None else ""
            ])

        if(len(data) == 0):
            print(colored.yellow("No optimizations available"))
            return

        table = columnar(data, headers=['Id', 'Name', 'Status', 'Preset', 'Parameters', 'Last Activity'], no_borders=True, wrap_max=13)
        print(table)

    def do_create_optimization(self, arg):
        '''Create an optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [
            {
                "type": "input", 
                "message": "Optimization name:", 
                "name": "name",
                "validate": lambda result: len(result) > 3,
                "invalid_message": "Invalid optimization name",
            },
            {
                "type": "list",
                "message": "Output format:",
                "name": "format",
                "choices": [
                    Choice("format_obj", name="obj"),
                    Choice("format_fbx", name="fbx"),
                    Choice("format_stl", name="stl"),
                    Choice("format_3ds", name="3ds"),
                ],
                "multiselect": False,
            },
        ]

        name_format = prompt(questions)
        print(name_format)

        questions = [
            {
                "type": "confirm",
                "message": "Do you want to use a preset?",
                "name": "confirm",
                "default": True,
            },
        ]

        preset_confirm = prompt(questions)
        print(preset_confirm)

        if preset_confirm['confirm']:
            questions = [
                {
                    "type": "list",
                    "message": "Preset:",
                    "name": "preset",
                    "choices": [
                        Choice("low", name="low"),
                        Choice("medium", name="medium"),
                        Choice("high", name="high"),
                    ],
                    "multiselect": False,
                },
            ]

            preset = prompt(questions)
            print(preset)
        else:
            questions = [
                {
                    "type": "number",
                    "name": "face_reduction",
                    "instruction": "0 - 0.999",
                    "message": "Face Reduction:",
                    "min_allowed": 0,
                    "max_allowed": 0.999,
                    "float_allowed": True,
                    "validate": EmptyInputValidator(),
                },
                {
                    "type": "number",
                    "name": "feature_importance",
                    "min_allowed": 0,
                    "max_allowed": 2,
                    "instruction": "0,1,2",
                    "message": "Feature Importance:",
                    "float_allowed": False,
                    "validate": EmptyInputValidator(),
                },
                {
                    "type": "confirm",
                    "message": "Preserve Boundary Edges",
                    "name": "preserve_boundary_edges",
                    "default": False,
                },
                {
                    "type": "confirm",
                    "message": "Preserve Hard Edges",
                    "name": "preserve_hard_edges",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Preserve Smooth Edges",
                    "name": "preserve_smooth_edges",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Retexture",
                    "name": "retexture",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Merge Duplicated UV",
                    "name": "merge_duplicated_uv",
                    "default": False,
                },
                {
                    "type": "confirm",
                    "message": "Remove Isolated Vertices",
                    "name": "remove_isolated_vertices",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Remove Non Manifold Faces",
                    "name": "remove_non_manifold_faces",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Remove Duplicated Faces",
                    "name": "remove_duplicated_faces",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Remove Duplicated Boundary Vertices",
                    "name": "remove_duplicated_boundary_vertices",
                    "default": True,
                },
                {
                    "type": "confirm",
                    "message": "Remove Degenerate Faces",
                    "name": "remove_degenerate_faces",
                    "default": True,
                },
            ]

            parameters = prompt(questions)
            print(parameters)
        
        name = name_format['name']
        format = OptimizationOutputFormat[name_format['format']]
        print(name)
        print(format)

        if preset_confirm['confirm']:
            preset = OptimizationPreset[preset['preset']]
            optimization = self._amaz3dclient.create_optimization(name, format, preset=preset)
        else:
            params = OptimizationParams(**parameters)
            optimization = self._amaz3dclient.create_optimization(name, format, params=params)

        print(colored.green("Optimization {0} created successfully".format(optimization.id)))
        pass

    def do_select_optimization(self, arg):
        '''Select an optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
        except ValueError as ex:
            print(colored.red(ex))
            return

        questions = [
            {
                "type": "input",
                "message": "Optimization id",
                "name": "id",
            },
        ]

        result = prompt(questions)

        try:
            self._amaz3dclient.select_an_optimization(**result)
            print(colored.green("Optimization {0} selected".format(result["id"])))
        except ValueError as ex:
            print(colored.red(ex))

    def do_download_selected_optimization(self, arg):
        '''Download selected optimization'''
        try:
            project = self._amaz3dclient.get_selected_project()
            optimization = self._amaz3dclient.get_selected_optimization()
        except ValueError as ex:
            print(colored.red(ex))
            return

        home_path = "~/" if os.name == "posix" else "C:\\"

        def file_name_validator(result) -> bool:
            if re.search(r'[^A-Za-z0-9_\-\\]',result):
                return False
            return True

        questions = [
            {
                "type": "input",
                "message": "File name",
                "name": "file_name",
                "validate": file_name_validator,
            },
            {
                "type": "filepath",
                "message": "Object",
                "name": "dst_path",
                "default": home_path,
                "only_directories": True,
            },
        ]

        result = prompt(questions)
        self._amaz3dclient.download_selected_optimization(**result)
        print(colored.green("Optimization {0} downloaded successfully".format(optimization.id)))

