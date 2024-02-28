import { request } from "@/utils/service"

/** 查 */
export function getTableDataApi(params) {
  return request({
    url: "perf/getAllScript",
    method: "get",
    params
  })
}


