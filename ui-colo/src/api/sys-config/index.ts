import {request} from "@/utils/service"

/**
 * 定义type
 */
export interface CreateOrUpdateTableRequestData {
  id?: string
  name: string
  status: number
}

export interface GetTableRequestData {
  name?: string
  size: number
  currentPage: number
}


// 返回值类型
export interface GetTableListData {
  id: string
  name: string
  status: number
  createTime: string
}

export type GetTableResponseData = ApiResponseData<{
  list: GetTableListData[]
  total: number
}>

export interface RequestDataByID {
  id: string
}
/**
 * 接口
 */
/** 增 */
export function createTableDataApi(data: CreateOrUpdateTableRequestData) {
  return request({
    url: "sysConfig/createConfig",
    method: "post",
    data
  })
}

export function deleteTableDataApi(data: RequestDataByID) {
  return request({
    url: "sysConfig/deleteConfig",
    method: "post",
    data
  })
}

export function updateTableDataApi(data:CreateOrUpdateTableRequestData) {
  return request({
    url: "sysConfig/updateConfig",
    method: "post",
    data
  })
}

/** 查 */
export function getTableDataApi(params: GetTableRequestData) {
  return request<GetTableResponseData>({
    url: "sysConfig/getConfig",
    method: "get",
    params
  })
}
