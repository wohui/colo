<script setup lang="ts">
import {reactive, ref, watch} from "vue";
import {CirclePlus, Delete, Refresh, RefreshRight, Search} from "@element-plus/icons-vue";
import {ElMessage, ElMessageBox, FormInstance, FormRules} from "element-plus";
import {usePagination} from "@/hooks/usePagination";
import {
  applyTestMachineApi,
  CreateOrUpdateTestMachineRequestData,
  createTestMachineApi,
  deleteTestMachineApi,
  GetTestMachineData,
  getTestMachineDataApi,
  updateTestMachineApi
} from "@/api/test-machine";


const loading = ref<boolean>(false)
const searchData = reactive({
  ip: "",
})
const DEFAULT_FORM_DATA: CreateOrUpdateTestMachineRequestData = {
  id: undefined,
  ip: '',
  hardware_info: 'CPU:    内存:   硬盘    ',
  owner: 'hui',
  status: 0,
}
const formData = ref<CreateOrUpdateTestMachineRequestData>(JSON.parse(JSON.stringify(DEFAULT_FORM_DATA)))
const dialogVisible = ref<boolean>(false)
const searchFormRef = ref<FormInstance | null>(null)
const formRef = ref<FormInstance | null>(null)
const isValidIP = (rule: any, value: any, callback: any) => {
  console.log(value)
  const ipPattern = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  if (ipPattern.test(value)) {
    callback()
  } else {
    callback(new Error('请输入合法的IP地址'))
  }
}
const formRules: FormRules<CreateOrUpdateTestMachineRequestData> = {
  ip: [{required: true, trigger: "blur", message: "请输入IP地址"}, {
    validator: isValidIP,
    required: true,
    trigger: 'blur'
  }],
}

const machineStatusOptionsValue = ref('')
const machineStatusOptions = ref([
  {
    value: 0,
    label: '空闲'
  },
  {
    value: 1,
    label: '被占用'
  },
  {
    value: 99,
    label: '异常'
  }
])
const {paginationData, handleCurrentChange, handleSizeChange} = usePagination()
const testMachineData = ref<GetTestMachineData[]>([])
const getTestMachineData = () => {
  loading.value = true
  getTestMachineDataApi({
    currentPage: paginationData.currentPage,
    size: paginationData.pageSize,
  })
    .then(({data}) => {
      paginationData.total = data.total
      console.log(data)
      testMachineData.value = data.list
    })
    .catch(() => {
      testMachineData.value = []
    })
    .finally(() => {
      loading.value = false
    })
}
const handleCreateOrUpdate = () => {
  formRef.value?.validate((valid: boolean, fields) => {
    if (!valid) return console.error("表单校验不通过", fields)
    loading.value = true
    const api = formData.value.id === undefined ? createTestMachineApi : updateTestMachineApi
    api(formData.value)
      .then(() => {
        ElMessage.success("操作成功")
        dialogVisible.value = false
        getTestMachineData()
      })
      .finally(() => {
        loading.value = false
      })
  })
}
const handleSearch = () => {
  paginationData.currentPage === 1 ? getTestMachineData() : (paginationData.currentPage = 1)
}
// 改
const handleUpdate = (row: GetTestMachineData) => {
  dialogVisible.value = true
  formData.value = JSON.parse(JSON.stringify(row))
}
const handleApply = (row: GetTestMachineData) => {
  ElMessageBox.confirm(`正在申请占用机器：${row.ip}，确认占用？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    applyTestMachineApi({id: row.id}).then(() => {
      ElMessage.success("占用成功")
      getTestMachineData()
    })
  })
}
const handleDelete = (row: GetTestMachineData) => {
  ElMessageBox.confirm(`正在删除机器：${row.ip}，确认删除？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    deleteTestMachineApi({id: row.id}).then(() => {
      ElMessage.success("删除成功")
      getTestMachineData()
    })
  })
}
const resetSearch = () => {
  searchFormRef.value?.resetFields()
}
const resetForm = () => {
  formRef.value?.clearValidate()
  formData.value = JSON.parse(JSON.stringify(DEFAULT_FORM_DATA))
}
/** 监听分页参数的变化 */
watch([() => paginationData.currentPage, () => paginationData.pageSize], getTestMachineData, {immediate: true})

</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never" class="search-wrapper">
      <el-form ref="searchFormRef" :inline="true" :model="searchData">
        <el-form-item prop="ip" label="机器地址">
          <el-input v-model="searchData.ip" placeholder="请输入"/>
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
          <el-button type="primary" :icon="CirclePlus" @click="dialogVisible = true">新增机器</el-button>
          <el-button type="danger" :icon="Delete">批量删除</el-button>
        </div>
        <div>
          <el-tooltip content="刷新当前页">
            <el-button type="primary" :icon="RefreshRight" circle @click="getTestMachineData"/>
          </el-tooltip>
        </div>
      </div>
      <div class="table-wrapper">
        <el-table :data="testMachineData">
          <el-table-column type="selection" width="50" align="center"/>
          <el-table-column prop="ip" label="IP" align="center"/>
          <el-table-column prop="hardware_info" label="硬件信息" align="center"/>
          <el-table-column prop="owner" label="负责人" align="center"/>
          <el-table-column prop="status" label="机器状态" align="center">
            <template #default="scope">
              <el-tag v-if="scope.row.status==0" size="large" type="success" effect="dark">空闲</el-tag>
              <el-tag v-else-if="scope.row.status==1" size="large" type="info" effect="dark">忙碌</el-tag>
              <el-tag v-else type="danger" size="large" effect="dark">异常</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" align="center"/>
          <el-table-column fixed="right" label="操作" width="240" align="center">
            <template #default="scope">
              <el-button type="primary" :disabled="scope.row.status !=0" @click="handleApply(scope.row)">申请占用
              </el-button>
              <el-button type="danger" :disabled="scope.row.status !=0" @click="handleDelete(scope.row)">刪除
              </el-button>
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
      :title="formData.id === undefined ? '新增机器' : '修改机器'"
      @closed="resetForm"
      width="25%"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="110px" label-position="left">
        <el-form-item prop="ip" label="机器地址" size="large">
          <el-input v-model="formData.ip" placeholder="请输入IP地址"/>
        </el-form-item>
        <el-form-item prop="hardware_info" label="硬件信息" size="large">
          <el-input v-model="formData.hardware_info" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="owner" label="负责人" size="large">
          <el-input v-model="formData.owner" placeholder="请输入"/>
        </el-form-item>
        <el-form-item prop="status" label="机器状态" size="large">
          <el-select
            v-model="formData.status"
            placeholder="Select"
            size="large"
            style="width: 240px"
          >
            <el-option
              v-for="item in machineStatusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrUpdate" :loading="loading">确认</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<style scoped lang="scss">
.search-wrapper {
  margin-bottom: 30px;

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
