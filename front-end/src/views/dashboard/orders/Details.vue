<template>
  <v-container fluid class="px-4 py-0">
    <template v-slot:after-heading> </template>
    <v-card class="pt-6">
      <div class="px-10 pb-5" height="800px">
        <v-row>
          <v-col cols="12" md="7">
            <v-row>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="temp.visit.customer_name"
                  color="yellow darken-3"
                  label="客户名称"
                  hint=""
                  required
                  disabled
                  prepend-icon="mdi-account-group"
                ></v-text-field
              ></v-col>
              <v-col cols="12" md="2">
                <v-autocomplete
                  v-model="temp.visit.visittype_id"
                  :items="visittypes"
                  item-text="name"
                  item-value="id"
                  label="拜访类型"
                  placeholder=""
                  prepend-icon="mdi-alpha-t-circle"
                  disabled
                ></v-autocomplete>
              </v-col>
              <v-col cols="12" md="2">
                <v-autocomplete
                  v-model="temp.status_code"
                  :items="statusCodes"
                  item-text="display_name"
                  item-value="key"
                  label="状态"
                  placeholder=""
                  prepend-icon="mdi-alpha-s-box"
                  disabled
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="7">
                <v-row>
                  <v-col cols="12" md="8">
                    <v-text-field
                      v-model="temp.document_code"
                      color="yellow darken-3"
                      label="档案编号"
                      hint=""
                      required
                      disabled
                      prepend-icon="mdi-file"
                    ></v-text-field
                  ></v-col>
                </v-row>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-autocomplete
                  v-model="temp.visit.contactorids"
                  :items="contactors"
                  item-text="name"
                  item-value="id"
                  label="联系人"
                  placeholder="本次拜访接待人员"
                  prepend-icon="mdi-account-search-outline"
                  multiple
                  chips
                  disabled
                ></v-autocomplete
              ></v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-autocomplete
                  v-model="temp.visit.address_id"
                  :items="addresses"
                  item-text="name"
                  item-value="id"
                  label="拜访地址"
                  placeholder=""
                  prepend-icon="mdi-alpha-t-circle"
                  disabled
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-divider class="mt-12" />
            <v-row>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="temp.visit.title"
                  color="yellow darken-3"
                  label="标题"
                  hint="简述此次拜访目的"
                  required
                  prepend-icon="mdi-subtitles"
                  disabled
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="temp.visit.author.name"
                  color="yellow darken-3"
                  label="创建者"
                  required
                  disabled
                  prepend-icon="mdi-account"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="12" md="5">
            <v-carousel
              cycle
              height="300"
              show-arrows-on-hover
              delimiter-icon="mdi-minus"
            >
              <v-carousel-item
                v-for="(attach, i) in temp.visit.attachments"
                :key="i"
              >
                <v-row class="fill-height" align="center" justify="center">
                  <v-img max-height="600" :src="attach.uri"></v-img>
                </v-row>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>

        <v-textarea
          v-model="temp.visit.description"
          color="yellow darken-3"
          label="描述拜访经过和成果"
          hint=""
          required
          prepend-icon="mdi-content-copy"
          auto-grow
          disabled
        ></v-textarea>
      </div>
      <div class="px-10 pb-5" height="800px">
        <v-timeline align-top :dense="$vuetify.breakpoint.smAndDown">
          <v-timeline-item
            v-for="(item, i) in temp.orderrecs"
            :key="i"
            fill-dot
            :color="colors[i]"
          >
            <v-card :color="colors[i]" dark>
              <v-card-title class="text-h6">
                {{ i + 1 }}. {{ item.nodename }}status_code:{{
                  item.status_code
                }}
              </v-card-title>
              <v-card-text class="white text--primary">
                <p>
                  {{ item.team.team_member }}
                </p>
                <p>
                  {{ item.opinion_text }}
                </p>
                <div
                  v-if="
                    canAudit(item.team.team_member) && item.status_code === 0
                  "
                >
                  <add-audit-dialog :orderrec-id="item.id" />
                </div>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import { fetchOrder, updateOrder } from '@/api/orders'
import {
  fetchVisittypesList,
  fetchContactorsListbyCustomerId,
  fetchAddressesListbyCustomerId,
} from '@/api/selections'

const statusCodes = [
  { key: 0, display_name: '新建' },
  { key: 1, display_name: '提审' },
  { key: 2, display_name: '完成' },
  { key: 3, display_name: '通过' },
  { key: 9, display_name: '驳回' },
]
export default {
  name: 'OrderDetails',
  components: {
    AddAuditDialog: () => import('./addAuditDialog'),
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
      statusCodes,
      listLoading: false,
      contactors: [],
      addresses: [],
      visittypes: [],
      details: null,
      temp: {
        attachments: [],
        visit: {
          author: {},
        },
      },
      rules: {},
      users: [],
      colors: [
        '#0099CC',
        '#FF6666',
        '#FFCCCC',
        '#0099CC',
        '#FF6666',
        '#FFCCCC',
      ],
    }
  },

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
    this.fetchData()
    this.getVisittypesList()
  },

  methods: {
    goBack() {
      this.$router.go(-1)
    },

    canAudit(arr) {
      const currentUserId = this.$store.getters.userId
      return arr.map(el => el.id).includes(currentUserId)
    },

    isAuthor(userId) {
      const currentUserId = this.$store.getters.userId
      return currentUserId === userId
    },

    fetchData() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      fetchOrder(id).then(response => {
        this.temp = response.data
        this.getContactorsListbyCustomerId(this.temp.visit.customer_id)
        this.getAddressesListbyCustomerId(this.temp.visit.customer_id)
        setTimeout(() => {
          this.listLoading = false
        }, 5 * 1000)
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

    editOrder() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      updateOrder(id, this.temp).then(response => {
        this.temp = response.data
        setTimeout(() => {
          this.listLoading = false
        }, 5 * 1000)
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
