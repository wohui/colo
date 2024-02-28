import { request } from "@/utils/service"
import type * as Table from "./types/planTable"

/** 增 */
export function createTableDataApi(data: Table.CreateOrUpdateTableRequestData) {
  return request({
    url: "perf/createPlan",
    method: "post",
    data
  })
}

/** 删 */
export function deleteTableDataApi(id: string) {
  return request({
    url: `table/${id}`,
    method: "delete"
  })
}

/** 改 */
export function updateTableDataApi(data: Table.CreateOrUpdateTableRequestData) {
  return request({
    url: "table",
    method: "put",
    data
  })
}

/** 查 */
export function getTableDataApi(params: Table.GetTableRequestData) {
  return request<Table.GetTableResponseData>({
    url: "perf/getPlanTableData",
    method: "get",
    params
  })
}

/**  */
export function executePerfPlanApi(data: Table.CreateOrUpdateTableRequestData) {
  return request <Table.CommonResponseData>({
    url: "perf/executePlan",
    method: "post",
    data
  })
}
