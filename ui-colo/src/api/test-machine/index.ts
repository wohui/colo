import {request} from "@/utils/service"

/**
 * 定义type
 */
export interface CreateOrUpdateTestMachineRequestData {
  id?: string
  ip: string
  hardware_info: string
  owner: string
  status: number
}

export interface GetTestMachineRequestData {
  name?: string
  size: number
  currentPage: number
}

export interface TestMachineRequetDataByID {
  id: string
}

// 返回值类型
export interface GetTestMachineData {
  createTime: string
  id: string
  ip: string
  hardware_info: string
  owner: string
  status: number
}

export type GetTestMachineResponseData = ApiResponseData<{
  list: GetTestMachineData[]
  total: number
}>

/**
 * 接口
 */
/** 增 */
export function createTestMachineApi(data: CreateOrUpdateTestMachineRequestData) {
  return request({
    url: "env/createTestMachine",
    method: "post",
    data
  })
}

export function deleteTestMachineApi(data: TestMachineRequetDataByID) {
  return request({
    url: "env/deleteTestMachine",
    method: "post",
    data
  })
}

export function applyTestMachineApi(data:TestMachineRequetDataByID) {
  return request({
    url: "env/applyTestMachine",
    method: "post",
    data
  })
}

export function updateTestMachineApi(data: CreateOrUpdateTestMachineRequestData) {
  return request({
    url: "env/updateTestMachine",
    method: "post",
    data
  })
}

/** 查 */
export function getTestMachineDataApi(params: GetTestMachineRequestData) {
  return request<GetTestMachineResponseData>({
    url: "env/getTestMachineData",
    method: "get",
    params
  })
}
