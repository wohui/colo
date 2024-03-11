<script lang="ts" setup>
import {reactive, ref, watch} from "vue"
import {
  createTableDataApi,
  deleteTableDataApi,
  executePerfPlanApi,
  getTableDataApi,
  updateTableDataApi
} from "@/api/plan"
import {type CreateOrUpdateTableRequestData, type GetTableData} from "@/api/plan/types/planTable"
import {ElMessage, ElMessageBox, type FormInstance, type FormRules} from "element-plus"
import {CirclePlus, Delete, Refresh, RefreshRight, Search} from "@element-plus/icons-vue"
import {usePagination} from "@/hooks/usePagination"
import {useRouter} from "vue-router";

defineOptions({
  // 命名当前组件
  name: "Plan"
})
const router = useRouter()
const loading = ref<boolean>(false)
const {paginationData, handleCurrentChange, handleSizeChange} = usePagination()

//#region 增
const DEFAULT_FORM_DATA: CreateOrUpdateTableRequestData = {
  id: undefined,
  name: "测试登录",
  host: "",
  script: "locustfile_1.py",
  user_count: 1,
  spawn_rate: 1,
  duration: '60',
  owner: "hui",
}
const planActiveIndex = ref('1')
const dialogVisible = ref<boolean>(false)
const formRef = ref<FormInstance | null>(null)
const formData = ref<CreateOrUpdateTableRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const formRules: FormRules<CreateOrUpdateTableRequestData> = {
  name: [{required: true, trigger: "blur", message: "请输入名称"}],
  host: [{required: true, trigger: "blur", message: "请输入完整接口URL"}],
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
const handleDelete = (row: GetTableData) => {
  ElMessageBox.confirm(`正在删除计划：${row.name}，确认删除？`, "提示", {
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
const handleUpdate = (row: GetTableData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
}
const handleExecute = (row: GetTableData) => {
  // 执行测试计划，生成测试记录
  openExecutePlanConfirmBox(row)
  // formData.value = JSON.parse(JSON.stringify(row))
}
const handleStop = (row: GetTableData) => {
  console.log(row)
  formData.value = JSON.parse(JSON.stringify(row))
}
//#endregion

//#region 查
const tableData = ref<GetTableData[]>([])
const searchFormRef = ref<FormInstance | null>(null)
const searchData = reactive({
  name: "",
})
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
// 传递的是表格对象的整行信息row
const executePerfPlan = (row: GetTableData) => {
  loading.value = true
  executePerfPlanApi(row)
      .then(({data}) => {
        router.push('/perf/testRecord')
      })
      .catch(() => {
        tableData.value = []
      })
      .finally(() => {
        loading.value = false
      })
}
const openExecutePlanConfirmBox = (row:GetTableData) => {
  ElMessageBox.confirm(
    '压测检查是否全部就绪，确认继续?',
    '警告',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      //确认后执行
      executePerfPlan(row)
      ElMessage({
        type: 'success',
        message: '执行成功',
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消执行',
      })
    })
}
const handlePlanMenuSelect = (key: string, keyPath: string[]) => {
  planActiveIndex.value = key
  console.log(key, keyPath)
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
        <el-form-item prop="name" label="测试计划">
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
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增计划</el-button>
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
          <el-table-column prop="name" label="计划名称" align="center"/>
          <el-table-column prop="owner" label="负责人" align="center"/>
          <el-table-column prop="user_count" label="并发用户数" align="center"/>
          <el-table-column prop="spawn_rate" label="每秒启动用户" align="center"/>
          <el-table-column prop="duration" label="压测时长（秒）" align="center"/>
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
              <el-button type="danger"  @click="handleDelete(scope.row)">删除</el-button>
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
        :title="formData.id === undefined ? '新增计划' : '修改计划'"
        @closed="resetForm"
        width="40%"
        height="50%"
    >
      <el-menu
          :default-active="planActiveIndex"
          class="el-menu-plan"
          mode="horizontal"
          @select="handlePlanMenuSelect"
      >
        <el-menu-item index="1">场景配置</el-menu-item>
        <el-menu-item index="2">压力配置</el-menu-item>
        <el-menu-item index="3">其他</el-menu-item>
      </el-menu>

      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="110px" label-position="left">
        <el-form-item prop="planName" label="计划名称" v-show="planActiveIndex=='1'" >
          <el-input v-model="formData.name" data-width="" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="host" label="目标环境" v-show="planActiveIndex=='1'">
          <el-input v-model="formData.host" placeholder="请输入主机或域名，eg.http://192.168.1.1/"/>
        </el-form-item>
        <el-form-item prop="script" label="压测脚本" v-show="planActiveIndex=='1'">
          <el-input v-model="formData.script" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="user_count" label="并发用户数" v-show="planActiveIndex=='2'">
          <el-input v-model="formData.user_count" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="spawn_rate" label="每秒启动用户" v-show="planActiveIndex=='2'">
          <el-input v-model="formData.spawn_rate" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="test_time" label="压测时长（秒）" v-show="planActiveIndex=='2'">
          <el-input v-model="formData.duration" placeholder="请输入"/>
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
.el-form {
  margin-top: 10px;
}
.el-form-item {
  width: 50%;
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
