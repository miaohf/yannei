<template>
  <v-dialog v-model="dialog" max-width="1000">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="green" dark v-bind="attrs" class="mx-1 my-2" v-on="on">
        新建 <v-icon right>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-container fluid>
      <v-card class="pt-10">
        <div class="px-6 pb-5" height="800px">
          <v-card-title class="pb-10"><h1>拜访日志</h1></v-card-title>
          <v-row>
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="temp.customer_id"
                :items="customers"
                item-text="name"
                item-value="id"
                label="客户名称"
                placeholder="选择公司或单位"
                prepend-icon="mdi-database-search"
                @change="
                  event => updateContactorsAndAddresses(event, temp.customer_id)
                "
              ></v-autocomplete
            ></v-col>

            <v-col cols="12" md="3"
              ><v-autocomplete
                v-model="temp.address_id"
                :items="addresses"
                item-text="name"
                item-value="id"
                label="地址"
                placeholder="本次拜访的客户地址"
                prepend-icon="mdi-account-search-outline"
              ></v-autocomplete
            ></v-col>

            <!-- <v-col cols="12" md="3">
              <v-autocomplete
                v-model="temp.visittype_id"
                :items="visittypes"
                item-text="name"
                item-value="id"
                label="拜访类型"
                placeholder=""
                prepend-icon="mdi-account-search-outline"
              ></v-autocomplete>
            </v-col> -->
            <!-- 拜访类型对应了审批流程，并决定了审批节点的数量和对应的审批团队和人员 -->
          </v-row>
          <v-row>
            <v-col
              ><v-autocomplete
                v-model="temp.contactorids"
                :items="contactors"
                item-text="name"
                item-value="id"
                label="联系人"
                placeholder="本次拜访接待人员"
                prepend-icon="mdi-account-search-outline"
                multiple
                chips
              ></v-autocomplete
            ></v-col>
          </v-row>

          <v-text-field
            v-model="temp.title"
            color="yellow darken-3"
            label="标题"
            hint="简述此次拜访目的和内容"
            required
          ></v-text-field>
          <v-textarea
            v-model="temp.description"
            color="yellow darken-3"
            label="描述拜访经过和成果"
            hint=""
            required
            auto-grow
          ></v-textarea>

          <v-row>
            <v-spacer></v-spacer>
            <span class="mt-6 mx-3" style="font-size:14px">
              技术支持<span class="yanei ml-1 mr-7">研一智控</span>
            </span>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="cancelAddDialog">取消</v-btn>
            <v-btn color="primary" @click="confirmAddDialog">确认</v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-container>
  </v-dialog>
</template>

<script>
import { createVisit } from '@/api/visits'
import {
  fetchCustomersList,
  fetchContactorsListbyCustomerId,
  fetchAddressesListbyCustomerId,
  // fetchVisittypesList,
} from '@/api/selections'

export default {
  name: 'AddVisitDialog',
  components: {},

  data: () => ({
    customers: [],
    contactors: [],
    addresses: [],
    visittypes: [],
    dialog: false,
    editdialog: false,
    temp: {
      title: '',
      description: '',
      visittype_id: '',
      customer_id: '',
      address_id: '',
      contactorids: [],
    },
  }),

  watch: {
    isUpdating(val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    },
  },
  mounted() {},
  created() {
    this.getCustomersList()
    // this.getVisittypesList()
  },
  methods: {
    getCustomersList() {
      fetchCustomersList().then(response => {
        this.customers = response.data.items
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
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

    // getVisittypesList() {
    //   fetchVisittypesList().then(response => {
    //     this.visittypes = response.data.items
    //     setTimeout(() => {
    //       this.listLoading = false
    //     }, 1.5 * 1000)
    //   })
    // },

    confirmAddDialog() {
      const tempData = this.temp
      createVisit(tempData).then(() => {
        this.dialog = false
        this.temp = {}
        this.$parent.getList()
      })
    },

    cancelAddDialog() {
      this.dialog = false
      this.temp = {}
    },

    updateContactorsAndAddresses(value, customerId) {
      this.getContactorsListbyCustomerId(customerId)
      this.getAddressesListbyCustomerId(customerId)
    },
  },
}
</script>

<style scoped lang="scss"></style>
