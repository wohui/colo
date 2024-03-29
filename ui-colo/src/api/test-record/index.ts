import { request } from "@/utils/service"
import type * as Table from "./types/table"
import {StopTestPlanRequestData} from "./types/table";

/** 查 */
export function getTableDataApi(params: Table.GetTableRequestData) {
  return request<Table.GetTableResponseData>({
    url: "perf/getTestRecord",
    method: "get",
    params
  })
}
export function stopExecutePlanApi(data:Table.StopTestPlanRequestData) {
  return request({
    url: "perf/stopExecutePlan",
    method: "post",
    data
  })
}


