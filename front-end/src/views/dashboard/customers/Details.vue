<template>
  <v-container fluid class="px-4 py-0">
    <template v-slot:after-heading> </template>
    <v-card class="pt-5" min-height="760px">
      <v-card-actions>
        <v-spacer />

        <v-btn v-show="!isEdit" color="red" @click="isEdit = !isEdit"
          >修改<v-icon right>mdi-text-box-edit</v-icon>
        </v-btn>
        <v-btn v-show="isEdit" color="info" @click="cancelEdit"
          ><v-icon>mdi-close-outline </v-icon></v-btn
        >
        <v-btn v-show="isEdit" color="green" @click="confirmEdit"
          ><v-icon text>mdi-check-outline</v-icon>
        </v-btn>
      </v-card-actions>
      <div class="px-5 pb-5">
        <v-row>
          <v-col cols="12" sm="4" md="4">
            <v-text-field
              v-model="temp.name"
              color="yellow darken-3"
              label="客户名称"
              required
              class="mx-6"
              :disabled="!isEdit"
              prepend-icon="mdi-account-search"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="4" md="4">
            <v-text-field
              v-model="temp.phone"
              color="yellow darken-3"
              label="公司电话"
              hint="请填写客户前台座机号码"
              required
              class="mx-6"
              :disabled="!isEdit"
              prepend-icon="mdi-phone-classic"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea
              v-model="temp.description"
              color="yellow darken-3"
              label="主营业务、客户概况、合作意向"
              hint=""
              required
              class="mx-6"
              :disabled="!isEdit"
              prepend-icon="mdi-text-search"
              auto-grow
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row class="mx-5">
          <v-expansion-panels accordion>
            <v-expansion-panel>
              <v-expansion-panel-header>
                <div>
                  <span v-show="isEdit">
                    <add-contactor-dialog @fetchData="fetchData"
                  /></span>
                  <v-icon left>mdi-account-circle</v-icon>

                  <v-badge color="primary" :content="temp.contactors.length">
                    联系人
                  </v-badge>
                </div>
              </v-expansion-panel-header>

              <v-expansion-panel-content>
                <span v-for="(item, i) in temp.contactors" :key="item.title">
                  <template>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-icon left color="primary"
                            >mdi-numeric-{{ i + 1 }}-circle-outline </v-icon
                          >{{ item.name }}</v-list-item-title
                        >
                        <v-list-item-subtitle> </v-list-item-subtitle>
                        <v-expansion-panel-content>
                          MOB: {{ item.mobile }}; PHO: {{ item.phone }}; POS:
                          {{ item.position }}; AGE: {{ item.age }}; SEX:
                          {{ item.sex }}; EML:{{ item.email }}; WEC:
                          {{ item.wechatid }}; EDU：{{ item.education_level }};
                          SCH: {{ item.graduated_school }}; SPO:
                          {{ item.spouse_detail }}; CHL:
                          {{ item.child_detail }}; ADR：{{
                            item.office_address
                          }}; DES: {{ item.description }}
                        </v-expansion-panel-content>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </span>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>

          <v-expansion-panels accordion>
            <v-expansion-panel>
              <v-expansion-panel-header>
                <div>
                  <span v-show="isEdit">
                    <add-address-dialog @fetchData="fetchData"
                  /></span>
                  <v-icon left>mdi-map-marker</v-icon>
                  <v-badge color="blue" :content="temp.addresses.length">
                    地址
                  </v-badge>
                </div>
              </v-expansion-panel-header>

              <v-expansion-panel-content>
                <span v-for="(item, i) in temp.addresses" :key="item.title">
                  <template>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-icon left color="blue"
                            >mdi-numeric-{{ i + 1 }}-circle-outline </v-icon
                          >{{ item.department }}</v-list-item-title
                        >
                        <v-list-item-subtitle>
                          {{ item.address_info }};{{ item.description }};
                          {{ item.province.name }};{{
                            item.city.name
                          }}</v-list-item-subtitle
                        >
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </span>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>

        <!-- <v-row v-show="isEdit" class="mx-5 mt-12">
          <v-spacer></v-spacer>
          <add-contactor-dialog />
          <add-address-dialog />
        </v-row> -->
      </div>
    </v-card>
  </v-container>
</template>

<script>
import { fetchCustomer, updateCustomer } from '@/api/customers'

export default {
  name: 'ContactorDetails',
  components: {
    AddContactorDialog: () => import('./addContactorDialog'),
    AddAddressDialog: () => import('./addAddressDialog'),
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
      provinces: [],
      cities: [],
      details: null,
      temp: {
        contactors: [],
        addresses: [],
      },
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
  },

  methods: {
    goBack() {
      this.$router.go(-1)
    },

    fetchData() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      fetchCustomer(id).then(response => {
        this.temp = response.data
        // this.getCitiesListByProvinceId(this.temp.province_id)
        setTimeout(() => {
          this.listLoading = false
        }, 5 * 1000)
      })
    },

    confirmEdit() {
      this.listLoading = true
      const id = this.$route.params && this.$route.params.id
      updateCustomer(id, this.temp).then(response => {
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
