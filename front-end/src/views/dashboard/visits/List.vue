<template>
  <v-container fluid class="px-4 py-0">
    <template v-slot:after-heading> </template>
    <v-row class="d-flex justify-space-between mx-1 mb-0">
      <div>
        <v-row>
          <v-switch
            v-model="listQuery.orderby_id_desc"
            label="倒序"
            style="max-width: 100px;"
            class="mx-3"
          ></v-switch>

          <v-select
            v-model="listQuery.customer_id"
            :items="customerOptions"
            item-text="display_name"
            item-value="key"
            menu-props="auto"
            hide-details
            label="客户名称"
            single-line
            class="mx-3"
            style="max-width: 80px;"
          ></v-select>

          <v-text-field
            v-model="listQuery.keyword"
            label="姓名"
            hide-details
            single-line
            class="mx-3"
            style="max-width: 120px;"
          />
        </v-row>
      </div>
      <div>
        <v-row class="mx-2"
          ><v-btn color="primary" class="mx-1 my-2" @click="getQuery">
            查询
            <v-icon right>mdi-magnify</v-icon>
          </v-btn>

          <v-btn color="primary" class="mx-1 mx-1 my-2" @click="resetQuery">
            重置
            <v-icon right>mdi-lock-reset</v-icon>
          </v-btn>

          <export-excel
            :fields="exportFields"
            worksheet="签约数据"
            name="九色鹿抽签签约数据.xls"
            :fetch="getListforExport"
          >
            <v-btn color="primary" class="mx-1 mx-1 my-2">
              导出
              <v-icon right>mdi-arrow-down-bold-circle-outline</v-icon>
            </v-btn>
          </export-excel>

          <div>
            <add-visit-dialog />
          </div>
        </v-row>
      </div>
    </v-row>

    <!-- <v-divider class="mt-3" /> -->

    <v-simple-table fixed-header class="pa-3" height="735px">
      <template v-slot:default>
        <thead>
          <tr>
            <th>ID</th>
            <th>档案编号</th>
            <th>标题</th>
            <th>公司(单位)名称</th>
            <th>拜访日志</th>
            <th>创建者</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>最后编辑</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in items" :key="row.id">
            <td
              class="font-weight-light grey--text text-left"
              style="font-size:11px"
            >
              {{ row.id }}
            </td>
            <td class="text-left">
              {{ row.document_code }}
            </td>
            <td class="text-left">
              {{ row.title | truncate(15) }}
            </td>
            <td class="text-left">
              {{ row.customer_name | truncate(15) }}
            </td>
            <!-- <td class="text-left">
              {{ row.contactor_name | truncate(15) }}
            </td> -->
            <td class="text-left">
              {{ row.description | truncate(40) }}
            </td>
            <td class="text-left">
              {{ row.author.name }}
            </td>
            <td class="text-left">
              <!-- {{ row.status_code }} -->
              {{ getNamefromOptions(statusCodes, row.status_code) }}
            </td>
            <td class="text-left">
              {{ $moment(row.create_at).format('YYYY-MM-DD HH:mm') }}
            </td>

            <td class="text-left">
              {{ $moment(row.last_update).format('YYYY-MM-DD HH:mm') }}
              <v-btn
                :color="icons.doc.color"
                icon
                fab
                x-small
                @click="handleToDetails(row)"
              >
                <v-icon right v-text="icons.doc.icon" />
              </v-btn>

              <v-btn
                v-if="isAuthor(row.author_id) && row.status_code === 0"
                :color="icons.delete.color"
                icon
                fab
                x-small
                @click="removeVisit(row)"
              >
                <v-icon right v-text="icons.delete.icon" />
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <v-pagination
      v-model="listQuery.page"
      :circle="circle"
      :disabled="disabled"
      :length="total_pages"
      :next-icon="nextIcon"
      :prev-icon="prevIcon"
      :total-visible="totalVisible"
      :value="listQuery.page"
      class="my-3"
      @input="paginationChangeHandler"
    ></v-pagination>
    <v-snackbar v-model="snackbar" :timeout="timeout">
      {{ text }}
    </v-snackbar>
  </v-container>
</template>

<script>
import {
  fetchVisits,
  // updateCustomer,
  deleteVisit,
} from '@/api/visits'

const statusCodes = [
  { key: 0, display_name: '新建' },
  { key: 1, display_name: '提审' },
  // { key: 2, display_name: '完成' },
  { key: 3, display_name: '完成' },
  { key: 9, display_name: '驳回' },
]

export default {
  name: 'Visits',

  components: {
    AddVisitDialog: () => import('./addVisitDialog'),
  },

  data: () => ({
    statusCodes,
    snackbar: false,
    text: '',
    timeout: 3000,
    panel: [0, 1],
    icons: {
      doc: {
        color: 'blue',
        icon: 'mdi-file-document',
      },
      delete: {
        color: 'warning',
        icon: 'mdi-trash-can',
      },
    },
    exportFields: {},
    items: [],
    listQuery: {
      page: 1,
      limit: 10,
      keyword: undefined,
      activity: undefined,
      batch_code: undefined,
      sort: '+id',
      orderby_id_desc: undefined,
    },
    search: '',
    awaitingSearch: false,
    circle: true,
    disabled: false,
    length: 10,
    nextIcon: 'mdi-chevron-right',
    prevIcon: 'mdi-chevron-left',
    totalVisible: 10,
    total_pages: 0,
    customerOptions: [],
  }),

  computed: {
    isAdminRole() {
      if (this.$store.getters.role.slug === 'administrator') {
        return true
      } else {
        return false
      }
    },
  },

  created() {
    this.getList()
    console.log(Date.now())
  },

  methods: {
    getQuery() {
      this.listQuery.page = 1
      this.getList()
    },

    isAuthor(authorId) {
      const currentUserId = this.$store.getters.userId
      return currentUserId === authorId
    },
    getList() {
      this.listLoading = true
      this.listQuery.limit = 10
      // this.listQuery.keyword = this.search

      fetchVisits(this.listQuery).then(response => {
        this.items = response.data.items
        this.total_pages = response.data._meta.total_pages

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    getListforExport() {
      this.listLoading = true
      this.listQuery.limit = 10000
      fetchVisits(this.listQuery).then(response => {
        this.exportItems = response.data.items
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
      return this.exportItems
    },

    resetQuery() {
      this.listQuery.keyword = undefined
      this.listQuery.batch_code = undefined
      this.listQuery.limit = 10
    },

    removeVisit(row) {
      this.$confirm('确认删除拜访日志?').then(res => {
        if (res) {
          deleteVisit(row.id).then(response => {
            this.getList()
            // Just to simulate the time of the request
            this.text = '拜访日志删除成功！'
            this.snackbar = true
          })
        }
      })
    },

    handleToDetails(row) {
      this.$router.push({
        name: 'VisitDetails',
        params: { id: row.id },
      })
    },

    getNamefromOptions(options, key) {
      let showname = ''
      options.forEach(item => {
        if (item.key === key) {
          showname = item.display_name
        }
      })
      return showname
    },

    paginationChangeHandler(pageNumber) {
      this.listQuery.page = pageNumber
      this.getList()
    },
  },
}
</script>

<style lang="scss" scoped>
th {
  font-size: 12px !important;
  font-weight: 800 !important;
}

tr:hover {
  background-color: #43b4dd !important;
  color: rgb(255, 255, 255);
}
</style>
