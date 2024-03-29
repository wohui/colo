export interface CreateOrUpdateTableRequestData {
  id?: string
  name: string
  host: string
  script: string
  user_count: number
  spawn_rate: number
  duration: string
  owner: string
}

export interface GetTableRequestData {
  /** 当前页码 */
  currentPage: number
  /** 查询条数 */
  size: number
  /** 查询参数：用户名 */
  name?: string
  /** 查询参数：手机号 */
  phone?: string
}

export interface GetTableData {
  createTime: string
  id: string
  status: boolean
  name: string
}

export type GetTableResponseData = ApiResponseData<{
  list: GetTableData[]
  total: number
}>

export type CommonResponseData = ApiResponseData<{
}>
