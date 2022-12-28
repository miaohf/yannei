<template>
  <v-dialog v-model="dialog" max-width="1200">
    <template v-slot:activator="{ on, attrs }">
      <v-btn text small color="blue" v-bind="attrs" class="mx-1 my-2" v-on="on">
        <v-icon>mdi-plus </v-icon>
      </v-btn>
    </template>
    <v-container>
      <v-card>
        <div class="px-7 pb-5" height="800px">
          <v-card-title class="my-10"><h1>新增客户地址</h1></v-card-title>
          <v-row>
            <v-col cols="12" sm="5" md="5">
              <v-text-field
                v-model="temp.department"
                color="yellow darken-3"
                label="部门名称"
                required
                class="mx-6"
                prepend-icon="mdi-domain"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="3" md="3">
              <v-autocomplete
                v-model="temp.province_id"
                :items="provinces"
                item-text="name"
                item-value="id"
                label="省份"
                placeholder="省份"
                prepend-icon="mdi-map-search"
                class="mx-6"
                @change="event => updateCities(event, temp.province_id)"
              ></v-autocomplete>
            </v-col>

            <v-col cols="12" sm="3" md="3">
              <v-autocomplete
                v-model="temp.city_id"
                :items="cities"
                item-text="name"
                item-value="id"
                label="城市"
                placeholder="城市"
                prepend-icon="mdi-city-variant"
                class="mx-6"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
                v-model="temp.address"
                color="yellow darken-3"
                label="坐落地址"
                hint="研一智控"
                required
                class="mx-6"
                prepend-icon="mdi-map-marker-plus"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-textarea
              v-model="temp.description"
              color="yellow darken-3"
              label="备注信息"
              hint=""
              required
              class="mx-6"
              prepend-icon="mdi-information-outline"
            ></v-textarea>
          </v-row>

          <v-row>
            <v-spacer></v-spacer>
            <span class="mt-6 mx-3 orange--text" style="font-size:14px">
              本系统由 研一智控 提供技术支持。
            </span>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="warning" @click="cancelAddDialog">取消</v-btn>
            <v-btn
              color="primary"
              :disabled="temp.address.length === 0"
              @click="confirmAddDialog"
              >确认</v-btn
            >
          </v-card-actions>
        </div>
      </v-card>
    </v-container>
  </v-dialog>
</template>

<script>
import { addContactorOrAddressByCustomer } from '@/api/customers'
import {
  fetchProvincesList,
  fetchCitesListbyProvinceID,
} from '@/api/selections'

export default {
  name: 'AddAddressDialog',
  components: {},

  data: () => ({
    provinces: [],
    cities: [],
    dialog: false,
    temp: {
      type: 'address',
      department: '',
      address: '',
      description: '',
    },
  }),
  mounted() {},
  created() {
    this.getProvincesList()
    console.log('AddAddressDialog $parent: ', this.$parent)
  },
  methods: {
    confirmAddDialog() {
      const id = this.$route.params.id
      const tempData = this.temp
      addContactorOrAddressByCustomer(id, tempData).then(() => {
        this.dialog = false
        this.temp = { type: 'address', address: '' }
        // this.$parent.$parent.fetchData()
        this.$emit('fetchData')
      })
    },

    cancelAddDialog() {
      this.dialog = false
      this.temp = { type: 'address', address: '' }
    },

    getProvincesList() {
      fetchProvincesList().then(response => {
        this.provinces = response.data.items
        console.log('this.provinces: ', this.provinces)
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    getCitiesListByProvinceId(id) {
      fetchCitesListbyProvinceID(id).then(response => {
        this.cities = response.data.items
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },

    updateCities(value, provinceId) {
      this.getCitiesListByProvinceId(provinceId)
    },
  },
}
</script>

<style scoped lang="scss"></style>
