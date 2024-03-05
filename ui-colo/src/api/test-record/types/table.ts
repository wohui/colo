

export interface GetTableRequestData {
  /** 当前页码 */
  currentPage: number
  /** 查询条数 */
  size: number
}
export interface StopTestPlanRequestData {
  /** 当前页码 */
  pid: number
}
export interface GetTableData {
  createTime: string
  pid: string
  status: boolean
  plan_name: string
  duration: number
  owner: string
  monitor_url: string
}

export type GetTableResponseData = ApiResponseData<{
  list: GetTableData[]
  total: number
}>
