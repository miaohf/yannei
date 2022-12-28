<template>
  <v-container fluid class="px-4 py-0">
    <template v-slot:after-heading> </template>
    <v-row class="d-flex justify-space-between mx-1">
      <div>
        <v-row>
          <v-switch
            v-model="listQuery.orderby_id_desc"
            label="倒序"
            style="max-width: 100px;"
            class="mx-3"
          ></v-switch>

          <v-select
            v-model="listQuery.village_id"
            :items="villagesOptions"
            item-text="display_name"
            item-value="key"
            menu-props="auto"
            hide-details
            label="选择城市"
            single-line
            class="mx-3"
            style="max-width: 80px;"
          ></v-select>

          <v-text-field
            v-model="listQuery.keyword"
            label="公司或单位名称"
            hide-details
            single-line
            class="mx-3"
            style="max-width: 120px;"
          />
        </v-row>
      </div>
      <div>
        <v-row class="mx-2 mb-3"
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
            worksheet="客户数据"
            name="研一.xls"
            :fetch="getListforExport"
          >
            <v-btn color="primary" class="mx-1 mx-1 my-2">
              导出
              <v-icon right>mdi-arrow-down-bold-circle-outline</v-icon>
            </v-btn>
          </export-excel>

          <div>
            <add-customer-dialog />
          </div>
        </v-row>
      </div>
    </v-row>

    <v-simple-table fixed-header class="pa-3" height="735px">
      <template v-slot:default>
        <thead>
          <tr>
            <th>ID</th>
            <th>客户名称</th>
            <th>所在城市</th>
            <th>公司电话</th>
            <th>综合描述</th>
            <th>创建时间</th>
            <th>最后更新</th>
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
              {{ row.name | truncate(20) }}
            </td>
            <td class="text-left">
              {{ row.city_name }}
            </td>
            <td class="text-left">
              {{ row.phone }}
            </td>
            <td class="text-left">
              {{ row.description | truncate(40) }}
            </td>
            <td class="text-left">
              {{ $moment(row.create_at).format('YYYY-MM-DD HH:mm:ss') }}
            </td>
            <td class="text-left">
              {{ $moment(row.last_update).format('YYYY-MM-DD HH:mm:ss') }}
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
                v-if="isAdminRole"
                :color="icons.delete.color"
                icon
                fab
                x-small
                @click="removeCustomer(row)"
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
  fetchCustomers,
  // updateCustomer,
  deleteCustomer,
} from '@/api/customers'

const batchCodeOptions = []

const villagesOptions = []

export default {
  name: 'Contracts',

  components: {
    AddCustomerDialog: () => import('./addCustomerDialog'),
  },

  data: () => ({
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
    exportItems: [],
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
    exportFields: {},

    greenColor: 'rgb(81, 185, 116)',
    warningColor: 'rgb(241, 211, 171)',
    batchCodeOptions,
    villagesOptions,
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

  // events: {
  //   eventGetlist: function(data) {
  //     console.log('eventGetlist')
  //   }
  // },
  // watch: {
  //     search: function (val) {
  //       if (!this.awaitingSearch) {
  //         setTimeout(() => {
  //           this.getList()
  //           this.awaitingSearch = false
  //         }, 1500); // 1 sec delay
  //       }
  //       this.awaitingSearch = true
  //     },
  //   },
  methods: {
    handleToDetails(row) {
      this.$router.push({
        name: 'CustomerDetails',
        params: { id: row.id },
      })
    },
    getQuery() {
      this.listQuery.page = 1
      this.getList()
    },

    getList() {
      this.listLoading = true
      this.listQuery.limit = 10
      // this.listQuery.keyword = this.search

      fetchCustomers(this.listQuery).then(response => {
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
      fetchCustomers(this.listQuery).then(response => {
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

    removeCustomer(row) {
      this.$confirm('确认删除客户档案?').then(res => {
        if (res) {
          deleteCustomer(row.id).then(response => {
            this.getList()
            // Just to simulate the time of the request
            this.text = '客户档案删除成功！'
            this.snackbar = true
          })
        }
      })
    },
    paginationChangeHandler(pageNumber) {
      this.listQuery.page = pageNumber
      this.getList()
    },
    // reset() {
    //   this.$refs.form.reset()
    // },
    // resetValidation() {
    //   this.$refs.form.resetValidation()
    // },
  },
}
</script>

<style lang="scss" scoped>
th {
  font-size: 12px !important;
  font-weight: 800;
}

// .background-transparent {
//   background-color: transparent !important;
// }

tr:hover {
  background-color: #43b4dd !important;
  color: rgb(255, 255, 255);
}
</style>
