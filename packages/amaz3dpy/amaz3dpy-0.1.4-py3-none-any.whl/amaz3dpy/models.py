from codecs import strict_errors
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class StringFieldComparison(BaseModel):
  eq: Optional[str]

class LoginInput(BaseModel):
    email: Optional[str]
    password: Optional[str]

class LoginOutput(BaseModel):
    token: Optional[str]
    refreshToken: Optional[str]

class RefreshInput(BaseModel):
    refreshToken: Optional[str]

class PageInfo(BaseModel):
    hasNextPage: Optional[bool]
    hasPreviousPage: Optional[bool]
    startCursor: Optional[str]
    endCursor: Optional[str]

class CursorPaging(BaseModel):
    before: Optional[str]
    after: Optional[str]
    first: Optional[int]
    last: Optional[int]

class ProjectFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    conversionStatus: Optional[StringFieldComparison]
    optimizationsCount: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    iname: Optional[StringFieldComparison]

class ProjectSort(BaseModel):
    field: Optional[str]
    direction: Optional[str]
    nulls: Optional[str]

class OptimizationSort(BaseModel):
  field: Optional[str]
  direction: Optional[str]
  nulls: Optional[str]

class ObjectModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    path: Optional[str]
    publicUrl: Optional[str]
    publicUrlExpiresAt: Optional[str]
    fileSizeBytes: Optional[int]
    triangleCount: Optional[int]

class Project(BaseModel):
    id: Optional[str]
    name: Optional[str]
    customerId: Optional[str]
    conversionStatus: Optional[str]
    optimizationsCount: Optional[int]
    conversionError: Optional[str]
    lastActivityAt: Optional[str]
    objectModel: Optional[ObjectModel]

class ProjectEdge(BaseModel):
    node: Project
    cursor: Optional[str]

class ProjectConnection(BaseModel):
    pageInfo: Optional[PageInfo]
    edges: Optional[List[ProjectEdge]]

class RelationId(BaseModel):
    id: Optional[str]

class ProjectCreateDto(BaseModel):
    name: Optional[str]
    objectModel: Optional[RelationId]
    customer: Optional[RelationId]

class OptimizationParams(BaseModel):
    face_reduction: Optional[float]
    feature_importance: Optional[int]
    preserve_boundary_edges: Optional[bool]
    preserve_hard_edges: Optional[bool]
    preserve_smooth_edges: Optional[bool]
    retexture: Optional[bool]
    merge_duplicated_uv: Optional[bool]
    remove_isolated_vertices: Optional[bool]
    remove_non_manifold_faces: Optional[bool]
    remove_duplicated_faces: Optional[bool]
    remove_duplicated_boundary_vertices: Optional[bool]
    remove_degenerate_faces: Optional[bool]

class OptimizationFilterProjectFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    conversionStatus: Optional[StringFieldComparison]
    optimizationsCount: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]

class OptimizationSort(BaseModel):
    field: Optional[str]
    direction: Optional[str]
    nulls: Optional[str]

class OptimizationFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    status: Optional[StringFieldComparison]
    createdAt: Optional[StringFieldComparison]
    updatedAt: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    project: Optional[OptimizationFilterProjectFilter]

class Optimization(BaseModel):
    id: Optional[str]
    name: Optional[str]
    status: Optional[str]
    outputFormat: Optional[str]
    preset: Optional[str]
    params: Optional[OptimizationParams]
    objectModelResult: Optional[ObjectModel]
    objectModelResultObj: Optional[ObjectModel]
    createdAt: Optional[str]
    updatedAt: Optional[str]
    lastActivityAt: Optional[str]
    project: Optional[Project]

class OptimizationEdge(BaseModel):
    node: Optional[Optimization]
    cursor: Optional[str]

class OptimizationConnection(BaseModel):
    pageInfo: Optional[PageInfo]
    edges: Optional[List[OptimizationEdge]]

class OptimizationParamsInput(BaseModel):
    face_reduction: Optional[float] = 0.5
    feature_importance: Optional[int] = 0
    preserve_boundary_edges: Optional[bool] = False
    preserve_hard_edges: Optional[bool] = True
    preserve_smooth_edges: Optional[bool] = True
    retexture: Optional[bool] = True
    merge_duplicated_uv: Optional[bool]
    remove_isolated_vertices: Optional[bool] = True
    remove_non_manifold_faces: Optional[bool] = True
    remove_duplicated_faces: Optional[bool] = True
    remove_duplicated_boundary_vertices: Optional[bool] = True
    remove_degenerate_faces: Optional[bool] = True

class OptimizationOutputFormat(str, Enum):
    format_obj = 'format_obj'
    format_gltf = 'format_gltf'
    format_stl = 'format_stl'
    format_3ds = 'format_3ds'
    format_fbx = 'format_fbx'

class OptimizationPreset(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class CreateOptimizationDto(BaseModel):
    name: Optional[str]
    outputFormat: Optional[OptimizationOutputFormat]
    preset: Optional[OptimizationPreset]
    project: Optional[RelationId]
    params: Optional[OptimizationParamsInput]

class CreateOneOptimizationInput(BaseModel):
    optimization: Optional[CreateOptimizationDto]

class ProjectDeleteResponse(BaseModel):
    id: Optional[str]
    name: Optional[str]
    customerId: Optional[str]
    conversionStatus: Optional[str]
    optimizationsCount: Optional[int]
    conversionError: Optional[str]
    lastActivityAt: Optional[str]