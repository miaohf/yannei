<template>
  <v-container id="register" class="fill-height justify-center" tag="section">
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
                注册页面
              </h1>
            </div>
          </template>

          <v-card-text class="text-center">
            <!-- <v-btn
              v-for="(social, i) in socials"
              :key="i"
              :color="social.iconColor"
              class="my-2 mr-1"
              dark
              depressed
              fab
              small
            >
              <v-icon v-text="social.icon" />
            </v-btn> -->

            <div class="my-2" />
            <v-form ref="registerForm" lazy-validation>
              <v-text-field
                v-model="registerForm.username"
                class="mb-8"
                color="secondary"
                label="Username ..."
                :counter="10"
                prepend-icon="mdi-face-man"
                required
              ></v-text-field>

              <v-text-field
                v-model="registerForm.name"
                class="mb-8"
                color="secondary"
                label="Your full name ..."
                :counter="10"
                prepend-icon="mdi-account"
                required
              ></v-text-field>

              <v-text-field
                v-model="registerForm.email"
                class="mb-8"
                color="secondary"
                label="Email ..."
                :counter="10"
                prepend-icon="mdi-email"
                required
              ></v-text-field>

              <v-text-field
                v-model="registerForm.password"
                class="mb-8"
                color="secondary"
                label="Password..."
                type="password"
                prepend-icon="mdi-lock-outline"
                required
                @keyup.enter.native="onSubmit"
              />

              <!-- <v-checkbox :input-value="true" color="secondary">
                <template v-slot:label>
                  <span class="text-no-wrap mr-2">I agree to the</span>

                  <a class="secondary--text ml-12 ml-sm-0" href="#">
                    terms and conditions </a
                  >.
                </template>
              </v-checkbox> -->

              <pages-btn color="success" class="mr-4" @click="onSubmit">
                提交注册
              </pages-btn>
            </v-form>
          </v-card-text>
        </base-material-card>
      </v-slide-y-transition>
    </v-row>
  </v-container>
</template>

<script>
import { createUser } from '@/api/users'
export default {
  name: 'PagesRegister',

  components: {
    PagesBtn: () => import('./components/Btn'),
    // PagesHeading: () => import('./components/Heading'),
  },

  data: () => ({
    registerForm: {
      username: '',
      name: '',
      email: '',
      password: '',
    },
    socials: [
      {
        href: '#',
        icon: 'mdi-wechat',
        iconColor: '#1DA1F2',
      },
    ],
  }),

  methods: {
    onSubmit(e) {
      this.registerForm.errors = 0 // 重置

      if (!this.registerForm.username) {
        this.registerForm.errors++
        this.registerForm.usernameError = 'Username required.'
      } else {
        this.registerForm.usernameError = null
      }

      if (!this.registerForm.name) {
        this.registerForm.errors++
        this.registerForm.nameError = 'name required.'
      } else {
        this.registerForm.nameError = null
      }

      if (!this.registerForm.email) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Email required.'
      } else if (!this.validEmail(this.registerForm.email)) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Valid email required.'
      } else {
        this.registerForm.emailError = null
      }

      if (!this.registerForm.password) {
        this.registerForm.errors++
        this.registerForm.passwordError = 'Password required.'
      } else {
        this.registerForm.passwordError = null
      }

      if (this.registerForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }
      const data = {
        confirm_email_base_url:
          window.location.href.split('/', 4).join('/') + '/unconfirmed/?token=',
        username: this.registerForm.username,
        name: this.registerForm.name,
        email: this.registerForm.email,
        password: this.registerForm.password,
      }
      createUser(data).then(response => {
        // console.log('createUser response: ', response)
        // handle success
        // this.$toasted.success(
        //   'A confirmation email has been sent to you by email.',
        //   { icon: 'fingerprint' }
        // )
        this.$router.push('/login')
      })
      // .catch(error => {
      //   // handle error
      //   // for (var field in error.response.data.message) {
      //   //   if (field === 'username') {
      //   //     this.registerForm.usernameError =
      //   //       error.response.data.message.username
      //   //   } else if (field === 'email') {
      //   //     this.registerForm.emailError = error.response.data.message.email
      //   //   } else if (field === 'password') {
      //   //     this.registerForm.passwordError =
      //   //       error.response.data.message.password
      //   //   }
      //   // }
      // })
    },
    validEmail: function(email) {
      var re = /^(([^<>()\\[\]\\.,;:\s@"]+(\.[^<>()\\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(email)
    },
  },
}
</script>

<style lang="sass">
#register
  .v-list-item__subtitle
    -webkic-line-clamp: initial
    -webkit-box-orient: initial
</style>
