<template>
  <v-container id="login" class="fill-height justify-center" tag="section">
    <v-row justify="left">
      <v-slide-y-transition appear>
        <base-material-card
          color="success"
          light
          max-width="100%"
          width="500"
          class="px-5 py-3"
        >
          <template v-slot:heading>
            <div class="text-center">
              <h1 class="text-h3 font-weight-bold mb-2">
                登录页面
              </h1>
            </div>
          </template>

          <v-card-text class="text-center">
            <v-form ref="loginForm" lazy-validation>
              <v-text-field
                v-model="loginForm.username"
                class="mb-8"
                color="secondary"
                label="请输入用户名"
                :counter="10"
                :rules="nameRules"
                prepend-icon="mdi-face-man"
                required
              ></v-text-field>

              <v-text-field
                v-model="loginForm.password"
                class="mb-8"
                color="secondary"
                label="请输入密码"
                type="password"
                prepend-icon="mdi-lock-outline"
                required
                @keyup.enter.native="handleLogin"
              />

              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-4"
                @click="handleLogin"
              >
                確定
              </v-btn>

              <v-btn color="error" class="mr-4" @click="reset">
                重置
              </v-btn>
            </v-form>
          </v-card-text>
        </base-material-card>
      </v-slide-y-transition>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    loginForm: {
      username: '',
      password: '',
    },
    valid: true,
    nameRules: [
      v => !!v || 'Name is required',
      v => (v && v.length <= 10) || 'Name must be less than 10 characters',
    ],
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
    select: null,
    items: ['Item 1', 'Item 2', 'Item 3', 'Item 4'],
    checkbox: false,
  }),

  created() {
    this.$vuetify.theme.dark = true
  },

  methods: {
    handleLogin() {
      console.log('handleLogin: ', this.loginForm)
      this.$refs.loginForm.validate(
        (this.loading = true),
        this.$store
          .dispatch('user/login', this.loginForm)
          .then(() => {
            this.$router.push({
              path: this.redirect || '/',
              query: this.otherQuery,
            })
            this.$store.dispatch('user/getInfo')
            this.loading = false
          })
          .catch(() => {
            this.loading = false
          })
      )
    },
    reset() {
      this.$refs.form.reset()
    },
    resetValidation() {
      this.$refs.form.resetValidation()
    },
  },
}
</script>
