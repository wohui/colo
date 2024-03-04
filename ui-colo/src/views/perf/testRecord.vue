<script lang="ts" setup>
import {onMounted, reactive, ref, watch} from "vue"
import {onBeforeRouteLeave, onBeforeRouteUpdate, useRoute} from "vue-router";
import {getTableDataApi, stopExecutePlanApi} from "@/api/test-record"
import {type GetTableData} from "@/api/test-record/types/table"
import {FormInstance} from "element-plus"
import {Refresh, RefreshRight, Search} from "@element-plus/icons-vue"
import {usePagination} from "@/hooks/usePagination"

defineOptions({
  // 命名当前组件
  name: "TestRecord"
})

const loading = ref<boolean>(false)
const {paginationData, handleCurrentChange, handleSizeChange} = usePagination()
//#region 查
const tableData = ref<GetTableData[]>([])
const searchData = reactive({
  name: "",
  phone: ""
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
const handleStop = (pid: number) => {
  loading.value = true
  stopExecutePlanApi({
    pid: pid,
  })
      .then((data) => {
        console.log(data)
      })
      .catch(() => {
      })
      .finally(() => {
        loading.value = false
      })
}

const handleSearch = () => {
  paginationData.currentPage === 1 ? getTableData() : (paginationData.currentPage = 1)
}

onMounted(() => {

  // getTableData()
})

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], getTableData, {immediate: true})

</script>
<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <el-form ref="searchFormRef" :inline="true" :model="searchData">
        <el-form-item prop="name" label="测试计划">
          <el-input v-model="searchData.name" placeholder="请输入"/>
        </el-form-item>
        <!--        <el-form-item prop="phone" label="手机号">-->
        <!--          <el-input v-model="searchData.phone" placeholder="请输入"/>-->
        <!--        </el-form-item>-->
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
          <el-button :icon="Refresh" @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
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
          <el-table-column prop="pid" label="进程ID" align="center"/>
          <el-table-column prop="plan_name" label="测试计划" align="center"/>
          <el-table-column prop="status" label="状态" align="center">
            <template #default="scope">
              <el-tag v-if="scope.row.status==1" type="primary" effect="plain">测试中</el-tag>
              <el-tag v-else-if="scope.row.status==2" type="success" effect="plain">测试完成</el-tag>
              <el-tag v-else type="danger" effect="plain">异常</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" align="center"/>
          <el-table-column fixed="right" label="操作" width="240" align="center">
            <template #default="scope">
              <el-button type="primary" text bg size="small"><a :href="scope.row.monitor_url" target="_blank">监控地址</a>
              </el-button>
              <el-button type="danger" :disabled="scope.row.status !=1" text bg size="small" @click="handleStop(scope.row.pid)">停止测试</el-button>
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
