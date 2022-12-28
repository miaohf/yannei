<template>
  <v-dialog v-model="dialog" max-width="1200">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="green" dark v-bind="attrs" class="mx-1 my-2" v-on="on">
        新建 <v-icon right>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-container>
      <v-card>
        <div class="px-7 pb-5" height="800px">
          <v-card-title class="my-10"><h1>新建客户资料</h1></v-card-title>
          <v-row>
            <v-col cols="12" sm="4" md="4">
              <v-text-field
                v-model="temp.name"
                color="yellow darken-3"
                label="客户名称"
                required
                class="mx-6"
                prepend-icon="mdi-account-search"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="4" md="4">
              <v-text-field
                v-model="temp.phone"
                color="yellow darken-3"
                label="电话号码"
                hint="请填写客户前台座机号码"
                required
                class="mx-6"
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
                auto-grow
                prepend-icon="mdi-text-search"
              ></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-spacer></v-spacer>
            <span class="mt-6 mx-3 orange--text" style="font-size:14px">
              本系统由 研一智控 提供技术支持。
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
import { createCustomer } from '@/api/customers'

export default {
  name: 'AddCustomerDialog',
  components: {},

  data: () => ({
    provinces: [],
    cities: [],
    dialog: false,
    temp: {
      name: '',
      description: '',
      phone: '',
      address: '',
      province_id: '',
      city_id: '',
    },
  }),
  mounted() {},
  created() {
    // this.getProvincesList()
  },
  methods: {
    // getProvincesList() {
    //   fetchProvincesList().then(response => {
    //     this.provinces = response.data.items
    //     console.log('this.provinces: ', this.provinces)
    //     setTimeout(() => {
    //       this.listLoading = false
    //     }, 1.5 * 1000)
    //   })
    // },

    // getCitiesListByProvinceId(id) {
    //   fetchCitesListbyProvinceID(id).then(response => {
    //     this.cities = response.data.items
    //     setTimeout(() => {
    //       this.listLoading = false
    //     }, 1.5 * 1000)
    //   })
    // },

    confirmAddDialog() {
      const tempData = this.temp
      console.log(tempData)
      createCustomer(tempData).then(() => {
        this.dialog = false
        this.temp = {}
        this.$parent.getList()
      })
    },

    cancelAddDialog() {
      this.dialog = false
      this.temp = {}
    },

    updateCities(value, provinceId) {
      console.log(value)
      console.log('provinceId: ', provinceId)
      this.getCitiesListByProvinceId(provinceId)
    },
  },
}
</script>

<style scoped lang="scss"></style>
