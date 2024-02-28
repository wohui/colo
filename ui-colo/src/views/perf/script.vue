<script lang="ts" setup>
import {reactive, ref, watch} from "vue"
import {
  getTableDataApi
} from "@/api/script"
import {ElMessage, ElMessageBox, FormInstance} from "element-plus"
import {CirclePlus, Delete, Refresh, RefreshRight, Search} from "@element-plus/icons-vue"
import {usePagination} from "@/hooks/usePagination"
import {stopExecutePlanApi} from "@/api/test-record";

defineOptions({
  // 命名当前组件
  name: "TestRecord"
})

const loading = ref<boolean>(false)
const {paginationData, handleCurrentChange, handleSizeChange} = usePagination()
//定义表格类型数据type
export interface GetTableData {
  createTime: string
  name1: string
  user1: string
  status: boolean
}
//#region 查
const tableData = ref<GetTableData[]>([])
const searchData = reactive({
  name: "",
})
const searchFormRef = ref<FormInstance | null>(null)
const resetSearch = () => {
  searchFormRef.value?.resetFields()
  handleSearch()
}
const getTableData = () => {
  loading.value = true
  getTableDataApi({
    currentPage: paginationData.currentPage,
    size: paginationData.pageSize,
    name: searchData.name || undefined,
  })
      .then(({data}) => {
        paginationData.total = data.total
        console.log(data)
        tableData.value = data.list
      })
      .catch(() => {
        tableData.value = []
      })
      .finally(() => {
        loading.value = false
      })
}

const handleSearch = () => {
  paginationData.currentPage === 1 ? getTableData() : (paginationData.currentPage = 1)
}
const handleStop = (pid) => {
  loading.value = true
  stopExecutePlanApi({
    pid: pid,
  })
      .then(({data}) => {
        console.log(data)
      })
      .catch(() => {
      })
      .finally(() => {
        loading.value = false
      })
}
/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], getTableData, {immediate: true})

</script>
<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <div class="toolbar-wrapper">
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="getTableData"/>
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="tableData">
          <el-table-column type="selection" width="50" align="center"/>
          <el-table-column prop="name1" label="脚本名称" align="center"/>
          <el-table-column prop="user1" label="维护人" align="center"/>
          <el-table-column prop="status" label="状态" align="center">
            <template #default="scope">
              <el-tag v-if="scope.row.status" type="success" effect="plain">启用</el-tag>
              <el-tag v-else type="danger" effect="plain">禁用</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" align="center"/>
          <el-table-column fixed="right" label="操作" width="240" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small" @click="handleStop(123)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pager-wrapper">
        <el-pagination
            background
            :layout="paginationData.layout"
            :page-sizes="paginationData.pageSizes"
            :total="paginationData.total"
            :page-size="paginationData.pageSize"
            :currentPage="paginationData.currentPage"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
.search-wrapper {
  margin-bottom: 20px;

  :deep(.el-card__body) {
    padding-bottom: 2px;
  }
}

.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.pager-wrapper {
  display: flex;
  justify-content: flex-end;
}
</style>
