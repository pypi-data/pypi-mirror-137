# Document

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**parent** | **int** |  | [optional] 
**parent_id** | **int** |  | [optional] 
**creator** | **int** |  | [optional] 
**project** | **int** |  | [optional] [readonly] 
**name** | **str** | Shown name of the file | 
**file_name** | **str** | Full name of the file | [optional] 
**description** | **str** | Description of the file | [optional] 
**file** | **str** |  | [optional] [readonly] 
**size** | **int** | Size of the file. | [optional] 
**created_at** | **datetime** | Creation date | [optional] [readonly] 
**updated_at** | **datetime** | Date of the last update | [optional] [readonly] 
**model_source** | **str** | Define the model.source field if the upload is a Model (IFC, PDF, DWG...) | [optional] 
**model_id** | **str** |  | [optional] [readonly] 
**ifc_source** | **str** | DEPRECATED: Use &#39;model_source&#39; instead. Define the model.source field if the upload is a Model (IFC, PDF, DWG...) | [optional] 
**ifc_id** | **str** | DEPRECATED: Use &#39;model_id&#39; instead. | [optional] [readonly] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


