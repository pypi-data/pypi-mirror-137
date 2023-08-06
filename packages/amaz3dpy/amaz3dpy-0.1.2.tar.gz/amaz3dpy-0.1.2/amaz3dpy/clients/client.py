
import threading
from amaz3dpy.auth import Auth
from amaz3dpy.projects import Projects
from amaz3dpy.models import LoginInput, Optimization, OptimizationOutputFormat, OptimizationParams, OptimizationPreset, Project
from amaz3dpy.optimizations import ProjectOptimizations

class Amaz3DClient():

    def check_project_selected(func):
        def wrapper(*args, **kwargs):
            if not args[0].__selected_project:
                raise ValueError("No project selected")
            return func(*args, **kwargs)
        return wrapper

    def check_optimization_selected(func):
        def wrapper(*args, **kwargs):
            if not args[0].__selected_optimization:
                raise ValueError("No optimization selected")
            return func(*args, **kwargs)
        return wrapper

    def synchronized(func):
        def _synchronized(self, *args, **kw):
            with self._lock: 
                return func(self, *args, **kw)
        return _synchronized

    def __listen(self):

        def project_received(project):
                pass

        def optimization_received(optimization: Optimization):
            with self._lock:
                project = self.__projects.get(optimization.project.id)

                if project is None:
                    print(optimization.project.id)
                    project = optimization.project
                    print(project)
                    self.__projects.add_existing_item(project)

                if optimization.project.id not in self.__project_optimizations.keys():
                    self.__project_optimizations[project.id] = ProjectOptimizations(self.__auth, project)
                
                project_optimizations = self.__project_optimizations[project.id]
                project_optimizations.add_existing_item(optimization)

        self.__projects.listen(project_received)
        self.__optimizatation_subscription.listen(optimization_received)

    def __stop_listen(self):
        self.__projects.stop_listen()
        self.__optimizatation_subscription.stop_listen()

    def __init__(self, url="amaz3d_backend.adapta.studio", use_ssl=True, disable_auto_update=False):
        self.__auth = Auth(url=url, use_ssl=use_ssl, refresh_token=True)
        self.__projects = Projects(self.__auth)
        self.__optimizatation_subscription = ProjectOptimizations(self.__auth)
        self.__project_optimizations = {}
        self.__selected_project = None
        self.__selected_optimization = None
        self._lock = threading.Lock()
        if self.__auth.token_value:
            self.__listen()

    def close(self):
        self.__stop_listen()

    def __del__(self):
        self.close()

    def login(self, email, password, keep_the_user_logged_in=True) -> bool:
        self.__auth.login_input = LoginInput(**{
            'email': email,
            'password': password,
        })
        if keep_the_user_logged_in:
            self.__auth.save_refresh_token()
        result = self.__auth.login()
        self.__listen()

        if result is not None:
            return True

        return False

    def logout(self):
        self.__auth.clear_credentials()
        self.__auth.clear_refresh_token()
        self.__auth.clear()

    def clear_configs(self):
        self.__auth.clear_configs()

    @synchronized
    def new_projects(self):
        return self.__projects.list_new()

    @synchronized
    def projects(self):
        return self.__projects.list()

    @synchronized
    def clear_projects(self):
        self.__projects.clear()

    @synchronized
    def load_projects(self):
        return self.__projects.load_next()

    @synchronized
    def load_project_by_id(self, id: str):
        return self.__projects.load_by_id(id)

    @synchronized
    def create_project(self, name: str, file_path: str) -> Project:
        return self.__projects.create_project(name=name, file_path=file_path)

    @synchronized
    @check_project_selected
    def delete_selected_project(self):
        self.__projects.delete_project(self.__selected_project)
        self.__selected_project = None

    @synchronized
    def select_a_project(self, id: str):
        selected = self.__projects.get(id)

        if selected is None:
            raise ValueError("Project not found")

        self.__selected_project = selected.id
        self.__selected_optimization = None

        if selected.id not in self.__project_optimizations.keys():
            self.__project_optimizations[selected.id] = ProjectOptimizations(self.__auth, selected)

        return self

    @synchronized
    @check_project_selected
    def get_selected_project(self):
        selected = self.__projects.get(self.__selected_project)

        if selected is None:
            raise ValueError("Project not found")

        return selected

    @synchronized
    @check_project_selected
    def optimizations(self):
        return self.__project_optimizations[self.__selected_project].list()

    @synchronized
    @check_project_selected
    def new_optimizations(self):
        return self.__project_optimizations[self.__selected_project].list_new()

    @synchronized
    @check_project_selected
    def delete_optimizations(self):
        self.__project_optimizations[self.__selected_project].clear()

    @synchronized
    @check_project_selected
    def load_optimizations(self):
        return self.__project_optimizations[self.__selected_project].load_next()

    @synchronized
    @check_project_selected
    def create_optimization(self, name, format: OptimizationOutputFormat, params: OptimizationParams = None, preset: OptimizationPreset = None):

        if params is None and preset is None:
            raise ValueError("EITHER parameters OR preset have to be provided")

        project_optimizations: ProjectOptimizations = self.__project_optimizations[self.__selected_project]

        if params:
            return project_optimizations.create_optimization(name=name, outputFormat=format, params=params)
            
        return project_optimizations.create_optimization(name=name, outputFormat=format, preset=preset)

    @synchronized
    @check_project_selected
    def select_an_optimization(self, id: str):
        selected = self.__project_optimizations[self.__selected_project].get(id)

        if selected is None:
            raise ValueError("Optimization not found in this project")

        self.__selected_optimization = selected.id
        return self

    def __get_selected_optimization(self):
        selected = self.__project_optimizations[self.__selected_project].get(self.__selected_optimization)

        if selected is None:
            raise ValueError("Optimization not found")

        return selected

    @synchronized
    @check_project_selected
    @check_optimization_selected
    def get_selected_optimization(self):
        return self.__get_selected_optimization()

    @synchronized
    @check_project_selected
    @check_optimization_selected
    def download_selected_optimization(self, dst_file_path=None, dst_path=None, file_name=None, add_extension=True):
        project_optimizations: ProjectOptimizations = self.__project_optimizations[self.__selected_project]
        optimization = self.__get_selected_optimization()
        project_optimizations.download_result(optimization, dst_file_path=dst_file_path, dst_path=dst_path, file_name=file_name, add_extension=add_extension)