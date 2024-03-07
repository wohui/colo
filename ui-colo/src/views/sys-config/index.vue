<script lang="ts" setup>
import {reactive, ref, watch} from "vue"
import {
  createTableDataApi,
  deleteTableDataApi,
  getTableDataApi, GetTableListData,
  updateTableDataApi
} from "@/api/sys-config"
import {ElMessage, ElMessageBox, type FormInstance, type FormRules} from "element-plus"
import {CirclePlus, Delete, Refresh, RefreshRight, Search} from "@element-plus/icons-vue"
import {usePagination} from "@/hooks/usePagination"
import {useRouter} from "vue-router";

defineOptions({
  // 命名当前组件
  name: "SysConfig"
})
const router = useRouter()
const loading = ref<boolean>(false)
const {paginationData, handleCurrentChange, handleSizeChange} = usePagination()

//#region 增
const DEFAULT_FORM_DATA: CreateOrUpdateTableRequestData = {
  id: undefined,
  name: "",
}
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateTableRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateTableRequestData> = {
  name: [{required: true, trigger: "blur", message: "请输入名称"}],
}
const handleCreateOrUpdate = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    loading.value = true
    const api = formData.value.id === undefined ? createTableDataApi : updateTableDataApi
    api(formData.value)
        .then(() => {
          ElMessage.success("操作成功")
          dialogVisible.value = false
          getTableData()
        })
        .finally(() => {
          loading.value = false
        })
  })
}
const resetForm = () => {
  formRef.value?.clearValidate()
  formData.value = JSON.parse(JSON.stringify(DEFAULT_FORM_DATA))
}
//#endregion

//#region 删
const handleDelete = (row: GetTableListData) => {
  ElMessageBox.confirm(`正在删除配置项：${row.name}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteTableDataApi(row.id).then(() => {
      ElMessage.success("删除成功")
      getTableData()
    })
  })
}
//#endregion

//#region 改
const handleUpdate = (row: GetTableListData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
}
const handleStop = (row: GetTableListData) => {
  console.log(row)
  formData.value = JSON.parse(JSON.stringify(row))
}
//#endregion

//#region 查
const tableData = ref<GetTableListData[]>([])
const searchFormRef = ref<FormInstance | null>(null)
const searchData = reactive({
  name: "",
  content: "{}",
})
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


const handleSearch = () => {
  paginationData.currentPage === 1 ? getTableData() : (paginationData.currentPage = 1)
}
const resetSearch = () => {
  searchFormRef.value?.resetFields()
  handleSearch()
}
//#endregion

/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], getTableData, {immediate: true})
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <el-form ref="searchFormRef" :inline="true" :model="searchData">
        <el-form-item prop="name" label="配置名称">
          <el-input v-model="searchData.name" placeholder="请输入"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
          <el-button :icon="Refresh" @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card v-loading="loading" shadow="never">
      <div class="toolbar-wrapper">
        <div>
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增配置</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="getTableData"/>
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="tableData">
          <el-table-column type="selection" width="50" align="center"/>
          <el-table-column prop="id" label="ID" width="50" align="center"/>
          <el-table-column prop="name" label="计划名称" align="center"/>
          <el-table-column prop="content" label="内容" align="center">
            <template #default="scope">
              <span>{{JSON.stringify(scope.row.content)}}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" align="center">
            <template #default="scope">
              <el-tag v-if="scope.row.status ==0" type="success" effect="plain">启用</el-tag>
              <el-tag v-else type="danger" effect="plain">禁用</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" align="center"/>
          <el-table-column fixed="right" label="操作" width="260" align="center">
            <template #default="scope">
              <el-button type="primary"  @click="handleExecute(scope.row)">开始压测</el-button>
              <el-button type="primary"   @click="handleUpdate(scope.row)">修改</el-button>
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
    <!-- 新增/修改 -->
    <el-dialog
        v-model="dialogVisible"
        :title="formData.id === undefined ? '新增配置' : '修改配置'"
        @closed="resetForm"
        width="40%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="110px" label-position="left">
        <el-form-item prop="name" label="配置名称">
          <el-input v-model="formData.name" placeholder="请输入"/>
        </el-form-item>
          <el-form-item prop="content" label="内容">
          <el-input v-model="formData.content" placeholder="请输入json格式"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdate" :loading="loading">确认</el-button>
      </template>
    </el-dialog>
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
