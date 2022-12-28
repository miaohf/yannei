<template>
  <v-dialog v-model="dialog" max-width="1200">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        text
        small
        color="primary"
        v-bind="attrs"
        class="mx-1 my-2"
        v-on="on"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-container>
      <v-card>
        <div class="px-7 pb-5" height="800px">
          <v-card-title class="my-6"><h1>新增客户联系人</h1></v-card-title>
          <v-subheader class="mx-2">基本信息</v-subheader>
          <v-row>
            <v-col cols="12" sm="3" md="3">
              <v-text-field
                v-model="temp.name"
                color="yellow darken-3"
                label="姓名"
                hint="填写客户联系人姓名"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="1" md="1">
              <v-text-field
                v-model="temp.age"
                color="yellow darken-3"
                label="年龄"
                hint=""
                required
                class="mx-6"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="2" md="2">
              <v-select
                v-model="temp.sex"
                :items="sexOptions"
                item-text="display_name"
                item-value="key"
                menu-props="auto"
                hide-details
                label="性别"
                single-line
                class="mx-6"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="2" md="2">
              <v-select
                v-model="temp.education_level"
                :items="educationLevels"
                item-text="display_name"
                item-value="key"
                menu-props="auto"
                hide-details
                label="教育"
                single-line
                class="mx-6"
              ></v-select>
            </v-col>

            <v-col cols="12" sm="4" md="4">
              <v-text-field
                v-model="temp.position"
                color="yellow darken-3"
                label="职位描述"
                hint="填写受访者当前职务后者项目中的角色"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-subheader class="mx-2">联系资料</v-subheader>
          <v-row>
            <v-col cols="12" sm="2" md="2">
              <v-text-field
                v-model="temp.mobile"
                color="yellow darken-3"
                label="移动电话"
                hint="填写联系人个人移动电话号码"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="2" md="2">
              <v-text-field
                v-model="temp.phone"
                color="yellow darken-3"
                label="固定电话"
                hint="填写联系人办公固话号码"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="2" md="2">
              <v-text-field
                v-model="temp.weichatid"
                color="yellow darken-3"
                label="微信"
                hint="填写客户微信号或者微信绑定的手机号"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="3" md="3">
              <v-text-field
                v-model="temp.email"
                color="yellow darken-3"
                label="邮箱地址"
                hint="填写邮箱地址"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="3" md="3">
              <v-text-field
                v-model="temp.office_address"
                color="yellow darken-3"
                label="办公地址"
                hint="填写办公室所在楼幢、楼层、门牌号等"
                required
                class="mx-6"
              ></v-text-field>
            </v-col>
          </v-row>

          <!-- <v-subheader class="mx-2">附加信息</v-subheader> -->
          <v-expansion-panels accordion>
            <v-expansion-panel>
              <v-expansion-panel-header>其他信息</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-col>
                    <v-textarea
                      v-model="temp.graduated_school"
                      color="yellow darken-3"
                      label="毕业情况（选填）"
                      hint="填写联系人毕业院校、毕业年份等信息"
                      required
                      class="mx-6"
                    ></v-textarea>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-textarea
                      v-model="temp.spouse_detail"
                      color="yellow darken-3"
                      label="配偶情况（选填）"
                      hint="填写联系人配偶教育、工作等信息"
                      required
                      class="mx-6"
                    ></v-textarea>

                    <v-textarea
                      v-model="temp.child_detail"
                      color="yellow darken-3"
                      label="子女情况（选填）"
                      hint="填写联系人子女教育、工作相关情况"
                      required
                      class="mx-6"
                    ></v-textarea>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" sm="12" md="12">
                    <v-textarea
                      v-model="temp.description"
                      color="yellow darken-3"
                      label="其他备注（选填）"
                      hint="填写联系人其他信息"
                      required
                      class="mx-6"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>

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
              :disabled="temp.name.length === 0"
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
const educationLevels = [
  { key: 1, display_name: '高中' },
  { key: 2, display_name: '中专' },
  { key: 3, display_name: '大专' },
  { key: 4, display_name: '本科' },
  { key: 5, display_name: '硕士' },
  { key: 6, display_name: '博士' },
  { key: 7, display_name: '教授' },
]

const sexOptions = [
  { key: 0, display_name: '男' },
  { key: 1, display_name: '女' },
]
export default {
  name: 'AddCustomerDialog',
  components: {},

  data: () => ({
    educationLevels,
    sexOptions,
    provinces: [],
    cities: [],
    dialog: false,
    temp: {
      type: 'contactor',
      name: '',
      description: '',
      phone: '',
    },
  }),
  mounted() {},
  created() {},
  methods: {
    confirmAddDialog() {
      // console.log('this.temp.name.length: ', this.temp.name.length)
      const id = this.$route.params.id
      const tempData = this.temp
      addContactorOrAddressByCustomer(id, tempData).then(() => {
        this.dialog = false
        this.temp = { type: 'contactor', name: '' }

        // this.$parent.$parent.fetchData()
        this.$emit('fetchData')
      })
    },

    cancelAddDialog() {
      this.dialog = false
      this.temp = { type: 'contactor', name: '' }
    },
  },
}
</script>

<style scoped lang="scss"></style>
