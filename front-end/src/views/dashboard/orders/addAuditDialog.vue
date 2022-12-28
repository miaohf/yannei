<template>
  <v-dialog v-model="dialog" max-width="1000">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="green" dark v-bind="attrs" class="mx-1 my-2" v-on="on">
        审批 <v-icon right>mdi-stamper</v-icon>
      </v-btn>
    </template>
    <v-container fluid>
      <v-card class="pt-10">
        <div class="px-6 pb-5" height="800px">
          <v-card-title class="pb-10"><h1>日志审批</h1></v-card-title>

          <v-textarea
            v-model="temp.opinion_text"
            color="yellow darken-3"
            label="填写审批意见"
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
            <v-btn color="primary" @click="cancelAudit">取消</v-btn>
            <v-btn color="primary" @click="rejectAudit(orderrecId)">驳回</v-btn>
            <v-btn color="primary" @click="confirmAudit(orderrecId)"
              >通过</v-btn
            >
          </v-card-actions>
        </div>
      </v-card>
    </v-container>
  </v-dialog>
</template>

<script>
import { updateOrderrec } from '@/api/orderrecs'

export default {
  name: 'AddAuditDialog',
  components: {},
  // props: ['orderrecId'],
  // props: { orderrecId: String },
  props: {
    orderrecId: {
      type: Number,
      requires: true,
      default: 0,
    },
  },
  data: () => ({
    dialog: false,

    temp: {
      status_code: '',
      opinion_text: '',
    },
  }),

  watch: {},
  mounted() {},
  created() {},
  methods: {
    rejectAudit(id) {
      this.temp.status_code = 9
      const tempData = this.temp
      updateOrderrec(id, tempData).then(() => {
        this.dialog = false
        this.temp = {}
        this.$parent.fetchData()
      })
    },

    confirmAudit(id) {
      this.temp.status_code = 3
      const tempData = this.temp
      updateOrderrec(id, tempData).then(() => {
        this.dialog = false
        this.temp = {}
        // this.$parent.fetchData()

        this.$router.push({
          name: 'Order',
        })
      })
    },

    cancelAudit() {
      this.dialog = false
      this.temp = {}
    },
  },
}
</script>

<style scoped lang="scss"></style>
