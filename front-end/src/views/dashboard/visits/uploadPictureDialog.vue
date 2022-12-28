<template>
  <v-dialog v-model="dialog" max-width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="blue" v-bind="attrs" class="mx-5" v-on="on">
        上传照片 <v-icon right>mdi-upload </v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-actions v-if="image">
        <v-spacer></v-spacer>
        <v-btn color="info" icon x-large @click="cancelUpload"
          ><v-icon>mdi-close-outline </v-icon></v-btn
        >
        <v-btn color="primary" icon x-large @click="uploadFile"
          ><v-icon text>mdi-check-outline</v-icon></v-btn
        >
      </v-card-actions>
      <div class="text-center">
        <input ref="file" type="file" class="d-none" @change="onChange" />
        <v-card @click="$refs.file.click()">
          <v-img v-if="image" :src="image" />
          <v-icon v-else class="mx-auto" size="400">
            mdi-image-area
          </v-icon>
        </v-card>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
import { upload } from '@/api/upload'
export default {
  name: 'UploadPictureDialog',
  data() {
    return {
      dialog: false,
      image: null,
      uploadQuery: {
        id: undefined,
        filetype: 'image',
      },
    }
  },
  methods: {
    onChange(val) {
      const value = val.target.files[0]
      if (!value) return (this.image = null)
      this.image = URL.createObjectURL(value)
    },

    cancelUpload() {
      this.dialog = false
      this.image = null
    },

    uploadFile() {
      // 创建表单对象
      const data = new FormData()

      data.append('file', (this.file = this.$refs.file.files[0]))

      this.uploadQuery.id = this.$route.params.id
      upload(data, this.uploadQuery).then(() => {
        this.dialog = false
        this.$parent.$parent.fetchData()
        this.image = null
      })
    },
  },
}
</script>
