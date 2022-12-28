<template>
  <v-container fluid class="px-4 py-0">
    <template v-slot:after-heading> </template>
    <v-card class="pt-6" min-height="760px">
      <v-card-actions>
        <v-spacer></v-spacer>
        <div
          v-if="isEdit && temp.status_code === 0 && isAuthor(temp.author_id)"
          align="center"
          justify="center"
        >
          <upload-picture-dialog></upload-picture-dialog>
        </div>
        <v-btn
          v-show="!isEdit && temp.status_code === 0 && isAuthor(temp.author_id)"
          color="warning"
          @click="isEdit = !isEdit"
          >修改<v-icon right>mdi-text-box-edit</v-icon>
        </v-btn>
        <v-btn
          v-show="!isEdit && temp.status_code === 0 && isAuthor(temp.author_id)"
          color="primary"
          @click="submitAudit"
          >提交<v-icon right>mdi-check-bold</v-icon>
        </v-btn>
        <v-btn
          v-show="!isEdit && temp.status_code === 1 && isAuthor(temp.author_id)"
          color="warning"
          @click="cancelAudit"
          >撤回<v-icon right>mdi-check-bold</v-icon>
        </v-btn>
        <v-btn v-show="isEdit" color="info" @click="cancelEdit"
          ><v-icon>mdi-close-outline </v-icon></v-btn
        >
        <v-btn v-show="isEdit" color="green" @click="confirmEdit"
          ><v-icon text>mdi-check-outline</v-icon>
        </v-btn>
      </v-card-actions>
      <div class="px-10 pb-5">
        <v-row>
          <v-col cols="12" md="7">
            <v-row>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="temp.customer_name"
                  color="yellow darken-3"
                  label="客户名称"
                  hint=""
                  required
                  disabled
                  prepend-icon="mdi-account-group"
                ></v-text-field
              ></v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="temp.title"
                  color="yellow darken-3"
                  label="标题"
                  hint="简述此次拜访目的"
                  required
                  :disabled="!isEdit"
                  prepend-icon="mdi-subtitles"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  v-model="temp.author.name"
                  color="yellow darken-3"
                  label="创建者"
                  required
                  disabled
                  prepend-icon="mdi-account"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2">
                <v-autocomplete
                  v-model="temp.status_code"
                  :items="statusCodes"
                  item-text="display_name"
                  item-value="key"
                  label="当前状态"
                  placeholder=""
                  prepend-icon="mdi-alpha-s-box"
                  disabled
                ></v-autocomplete>
              </v-col>
            </v-row>
            <!-- <v-row>
              <v-col cols="12" md="2">
                <v-autocomplete
                  v-model="temp.status_code"
                  :items="statusCodes"
                  item-text="display_name"
                  item-value="key"
                  label="当前状态"
                  placeholder=""
                  prepend-icon="mdi-alpha-s-box"
                  disabled
                ></v-autocomplete>
              </v-col>
            </v-row> -->
            <v-row>
              <v-col>
                <v-textarea
                  v-model="temp.description"
                  color="yellow darken-3"
                  label="描述拜访经过和成果"
                  hint=""
                  required
                  :disabled="!isEdit"
                  prepend-icon="mdi-content-copy"
                  auto-grow
                ></v-textarea>
              </v-col>
            </v-row>

            <v-row>
              <!-- <v-col>
                <v-autocomplete
                  v-model="temp.visittype_id"
                  :items="visittypes"
                  item-text="name"
                  item-value="id"
                  label="拜访类型"
                  placeholder=""
                  prepend-icon="mdi-alpha-t-circle"
                  :disabled="!isEdit"
                ></v-autocomplete>
              </v-col> -->
              <!-- <v-col cols="12" md="4">
                <span v-for="(c, i) in temp.contactors" :key="i">
                  {{ c.name }}
                </span>
              </v-col>
              <v-col cols="12" md="4">
                <span>{{ temp.address.address_info }}</span>
              </v-col> -->
              <v-col>
                <v-autocomplete
                  v-model="temp.contactorids"
                  :items="contactors"
                  item-text="name"
                  item-value="id"
                  label="联系人"
                  placeholder="本次拜访接待人员"
                  prepend-icon="mdi-account-search-outline"
                  multiple
                  chips
                  :disabled="!isEdit"
                ></v-autocomplete>
              </v-col>

              <!-- <v-col>
                <v-autocomplete
                  v-model="temp.status_code"
                  :items="statusCodes"
                  item-text="display_name"
                  item-value="key"
                  label="审核节点"
                  placeholder=""
                  prepend-icon="mdi-alpha-p-circle"
                  disabled
                ></v-autocomplete>
              </v-col> -->
            </v-row>
            <v-row>
              <!-- <v-col>
                <v-autocomplete
                  v-model="temp.visittype_id"
                  :items="visittypes"
                  item-text="name"
                  item-value="id"
                  label="拜访类型"
                  placeholder=""
                  prepend-icon="mdi-alpha-t-circle"
                  :disabled="!isEdit"
                ></v-autocomplete>
              </v-col> -->
              <v-col>
                <v-autocomplete
                  v-model="temp.address_id"
                  :items="addresses"
                  item-text="name"
                  item-value="id"
                  label="拜访地址"
                  placeholder="本次拜访会面地址"
                  prepend-icon="mdi-account-search"
                  :disabled="!isEdit"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row v-if="temp.order">
              <v-col v-for="(orderrec, i) in temp.order.orderrecs" :key="i">
                <v-row>
                  <v-text-field
                    v-if="orderrec.auditor"
                    v-model="orderrec.auditor.name"
                    color="yellow darken-3"
                    label="审批人"
                    required
                    disabled
                    prepend-icon="mdi-subtitles"
                  ></v-text-field>
                  <v-text-field
                    v-model="orderrec.opinion_text"
                    color="yellow darken-3"
                    label="意见"
                    required
                    disabled
                    prepend-icon="mdi-subtitles"
                  ></v-text-field>
                </v-row>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="12" md="5">
            <v-carousel
              cycle
              height="600"
              show-arrows-on-hover
              delimiter-icon="mdi-minus"
            >
              <v-carousel-item v-for="(attach, i) in temp.attachments" :key="i">
                <v-row class="fill-height" align="center" justify="center">
                  <v-img max-height="600" :src="attach.uri"></v-img>
                </v-row>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import { fetchVisit, updateVisit } from '@/api/visits'
import {
  fetchContactorsListbyCustomerId,
  fetchAddressesListbyCustomerId,
  fetchVisittypesList,
} from '@/api/selections'
const statusCodes = [
  { key: 0, display_name: '新建' },
  { key: 1, display_name: '提审' },
  // { key: 2, display_name: '完成' },
  { key: 3, display_name: '完成' },
  { key: 9, display_name: '驳回' },
]

export default {
  name: 'VisitDetails',
  components: {
    UploadPictureDialog: () => import('./uploadPictureDialog'),
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger',
      }
      return statusMap[status]
    },
  },
  data() {
    return {
      listLoading: false,
      contactors: [],
      addresses: [],
      visittypes: [],
      statusCodes,
      details: null,
      temp: { author: '', attachments: [], order: { orderrecs: [] } },
      rules: {},
      users: [],
      isEdit: false,
    }
  },

  computed: {
    isAdminRole() {
      if (this.$store.getters.roles.includes('admin')) {
        return true
      } else {
        return false
      }
    },
  },

  created() {
    this.fetchData()
    this.getVisittypesList()
  },

  methods: {
    goBack() {
      this.$router.go(-1)
    },

    isAuthor(authorId) {
      const currentUserId = this.$store.getters.userId
      return currentUserId === authorId
    },

    fetchData() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      fetchVisit(id).then(response => {
        this.temp = response.data
        this.getContactorsListbyCustomerId(this.temp.customer_id)
        this.getAddressesListbyCustomerId(this.temp.customer_id)
        setTimeout(() => {
          this.listLoading = false
        }, 5 * 1000)
      })
    },

    submitAudit() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      const tempData = { status_code: 1 }
      this.$confirm('确认日志填写已完整并要提交审核?').then(res => {
        if (res) {
          updateVisit(id, tempData).then(response => {
            this.temp = response.data
            setTimeout(() => {
              this.listLoading = false
            }, 5 * 1000)
          })
        }
      })
    },

    cancelAudit() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      const tempData = { status_code: 0 }
      this.$confirm('确认撤销日志审核?').then(res => {
        if (res) {
          updateVisit(id, tempData).then(response => {
            this.temp = response.data
            setTimeout(() => {
              this.listLoading = false
            }, 5 * 1000)
          })
        }
      })
    },

    getContactorsListbyCustomerId(id) {
      fetchContactorsListbyCustomerId(id).then(response => {
        this.contactors = response.data.items
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    getAddressesListbyCustomerId(id) {
      fetchAddressesListbyCustomerId(id).then(response => {
        this.addresses = response.data.items
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    getVisittypesList() {
      fetchVisittypesList().then(response => {
        this.visittypes = response.data.items
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    confirmEdit() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      updateVisit(id, this.temp).then(response => {
        this.temp = response.data
        setTimeout(() => {
          this.listLoading = false
        }, 5 * 1000)
      })
      this.isEdit = !this.isEdit
    },

    getNamefromOptions(options, key) {
      // return options[key]
      let showname = ''
      options.forEach(item => {
        if (item.key === key) {
          // console.log(key, item.key, item.display_name)
          showname = item.display_name
        }
      })
      return showname
    },

    cancelEdit() {
      this.isEdit = !this.isEdit
      this.fetchData()
    },

    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
  },
}
</script>
<style scoped>
/* .v-overflow-btn .v-input__slot::before {
  border-color: grey !important;
} */
</style>
