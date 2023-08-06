import requests
import os
from gql import Client, gql
from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.webapiclients.gqlwebsocketsclient import GQLWebsocketsClient

from amaz3dpy.auth import Auth
from amaz3dpy.models import CreateOptimizationDto, CursorPaging, Optimization, OptimizationConnection, OptimizationFilter, OptimizationFilterProjectFilter, OptimizationOutputFormat, OptimizationParams, OptimizationPreset, OptimizationSort, RelationId, StringFieldComparison
from amaz3dpy.items import Paging

class OptimizationError(Exception):
    pass

class ProjectOptimizations(Paging):

    def __init__(self, auth: Auth, project = None):
        super().__init__(Optimization, OptimizationFilter, OptimizationSort)
        self._auth = auth
        self._project = project
        if self._project:
            self._project_id = project.id
        self.clear()

    @property
    def project_id(self):
        return self._project_id

    def clear_and_load(self, paging: CursorPaging, filter: OptimizationFilter, sorting: OptimizationSort) -> dict:
        self.clear()
        self.load(paging, filter, sorting)

    def load_next(self) -> int:
        if self._project_id:
            self._filter.project = OptimizationFilterProjectFilter()
            self._filter.project.id = StringFieldComparison()
            self._filter.project.id.eq = self._project_id

        return super().load_next()

    def download_result(self, optimization: Optimization, dst_file_path = None, dst_path = None, file_name = None, add_extension = True):
        if optimization.objectModelResult is None:
            raise ValueError("optimization doesn't have a result")

        r = requests.get(optimization.objectModelResult.publicUrl, allow_redirects=True)
        path = dst_file_path
        
        if dst_file_path is None:
            if dst_path is None:
                raise ValueError("EITHER dst_file_path OR dst_path have to be provided")
            
            ext = ""

            if add_extension:
                ext = optimization.outputFormat.replace("format_", ".")

            if file_name:
                path = os.path.join(dst_path, file_name + ext)
            else:
                path = os.path.join(dst_path, optimization.name + ext)

        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(r.content)

    def create_optimization(
        self, create_optimization: CreateOptimizationDto = None, 
        name: str = None, outputFormat: OptimizationOutputFormat = None, 
        params: OptimizationParams = None,
        preset: OptimizationPreset = None,
        project_id: str = None
    ) -> Optimization:

        if create_optimization is None:
            if name is None and outputFormat is None and (params is None or preset is None):
                raise ValueError("EITHER 'name', 'outputFormat', and one of 'params' and 'preset' OR 'create_optimization' must be provided")
            
            if project_id is None and self._project is None:
                raise ValueError("Project must be provided when calling this method. Please provide project_id or a project")

            create_optimization = CreateOptimizationDto()
            create_optimization.name = name
            create_optimization.outputFormat = outputFormat

            if params:
                create_optimization.params = params
            else:
                create_optimization.preset = preset

            create_optimization.project = RelationId()
            create_optimization.project.id = project_id or self._project_id


        query = gql(
            """
            mutation CreateOptimization($input: CreateOneOptimizationInput!) {
                createOneOptimization(input: $input) {
                    id
                    name
                    status
                    outputFormat
                    params {
                        face_reduction
                        feature_importance
                        preserve_boundary_edges
                        preserve_hard_edges
                        preserve_smooth_edges
                        retexture
                        merge_duplicated_uv
                        remove_isolated_vertices
                        remove_non_manifold_faces
                        remove_duplicated_faces
                        remove_duplicated_boundary_vertices
                        remove_degenerate_faces
                    }
                    preset
                    objectModelResult {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                    }
                    lastActivityAt
                    objectModelResultObj {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                    }
                    project {
                        id
                    }
                }
            }
            """
        )

        params = {
            "input": {
                "optimization": create_optimization.dict(exclude_unset=True)
            }
        }

        try:
            optimization = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, Optimization)
            self._store_item(optimization, id=optimization.id)
            return optimization
        except GQLHttpClientError as ex:
            raise OptimizationError("Unable to perform Optimization. Is your Project ready to be Optimized?")
        

    def _load_items(self, paging: CursorPaging, filter: OptimizationFilter, sort: OptimizationSort) -> dict:
        query = gql(
            """
            query Optimizations($paging: CursorPaging, $filter: OptimizationFilter, $sorting: [OptimizationSort!]) {
                items: optimizations(filter: $filter, paging: $paging, sorting: $sorting) {
                    pageInfo {
                        startCursor
                        endCursor
                        hasNextPage
                        hasPreviousPage
                    }
                    edges {
                        cursor
                        node {
                            id
                            name
                            status
                            outputFormat
                            params {
                                face_reduction
                                feature_importance
                                preserve_boundary_edges
                                preserve_hard_edges
                                preserve_smooth_edges
                                retexture
                                merge_duplicated_uv
                                remove_isolated_vertices
                                remove_non_manifold_faces
                                remove_duplicated_faces
                                remove_duplicated_boundary_vertices
                                remove_degenerate_faces
                            }
                            preset
                            objectModelResult {
                                id
                                name
                                path
                                picture {
                                    publicUrl
                                }
                                publicUrl
                                triangleCount
                                fileSizeBytes
                            }
                            lastActivityAt
                            objectModelResultObj {
                                id
                                name
                                path
                                picture {
                                    publicUrl
                                }
                                publicUrl
                                triangleCount
                                fileSizeBytes
                            }
                            project {
                                id
                            }
                        }
                    }
                }
            }
            """
        )

        params = {
            "paging": paging.dict(exclude_unset=True),
            "filter": filter.dict(exclude_unset=True),
            "sorting": sort.dict(exclude_unset=True)
        }

        try:
            items = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, OptimizationConnection)
            return items
        except GQLHttpClientError as ex:
            return 0

    async def _handle_subscription(self):
        subscription = gql(
            """
            subscription OptimizationUpdated {
                updatedOneOptimization {
                    id
                    name
                    status
                    outputFormat
                    params {
                        face_reduction
                        feature_importance
                        preserve_boundary_edges
                        preserve_hard_edges
                        preserve_smooth_edges
                        retexture
                        merge_duplicated_uv
                        remove_isolated_vertices
                        remove_non_manifold_faces
                        remove_duplicated_faces
                        remove_duplicated_boundary_vertices
                        remove_degenerate_faces
                    }
                    preset
                    objectModelResult {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                    }
                    lastActivityAt
                    objectModelResultObj {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                    }
                    project {
                        id
                    }
                }
            }
            """
        )

        async with Client(
            transport=GQLWebsocketsClient(self._auth.token, self._auth.url, self._auth.use_ssl).transport(), fetch_schema_from_transport=True,
        ) as session:
            async for result in session.subscribe(subscription):
                item = Optimization(**result["updatedOneOptimization"])
                self._store_item(item, item.id)
                self._on_item_received(item)