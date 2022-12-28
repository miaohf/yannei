<template>
  <v-app-bar id="app-bar" absolute app color="transparent" flat height="75">
    <v-btn
      class="mr-3"
      elevation="1"
      fab
      small
      @click="
        $vuetify.breakpoint.smAndDown
          ? setDrawer(!drawer)
          : $emit('input', !value)
      "
    >
      <v-icon v-if="value">
        mdi-view-quilt
      </v-icon>

      <v-icon v-else>
        mdi-dots-vertical
      </v-icon>
    </v-btn>

    <v-toolbar-title
      class="hidden-sm-and-down font-weight-light"
      v-text="$t($route.name)"
    />

    <v-spacer />

    <v-col cols="auto">
      <v-row class="font-weight-black ">您好，{{ user.name }}</v-row>
    </v-col>

    <v-col cols="auto">
      <v-btn icon @click="$vuetify.theme.dark = !$vuetify.theme.dark">
        <v-icon v-if="$vuetify.theme.dark">mdi-white-balance-sunny</v-icon>
        <v-icon v-else>mdi-weather-night</v-icon>
      </v-btn>
    </v-col>

    <v-menu
      bottom
      left
      offset-y
      origin="top right"
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn class="ml-2" min-width="0" text v-bind="attrs" v-on="on">
          <v-badge color="red" overlap bordered>
            <template v-slot:badge>
              <span>19</span>
            </template>
            <v-icon>mdi-bell</v-icon>
          </v-badge>
        </v-btn>
      </template>

      <v-list :tile="false" nav>
        <div>
          <app-bar-item v-for="(n, i) in notifications" :key="`item-${i}`">
            <v-list-item-title>
              <v-badge color="red" overlap bordered class="mr-3">
                <template v-slot:badge>
                  <span>{{ n.count }}</span>
                </template>
                <v-icon left>mdi-bell</v-icon>
              </v-badge>
              {{ n.text }}
            </v-list-item-title>
          </app-bar-item>
        </div>
      </v-list>
    </v-menu>

    <v-menu
      bottom
      left
      min-width="200"
      offset-y
      origin="top right"
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn class="ml-2" min-width="0" text v-bind="attrs" v-on="on">
          <v-icon left>mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list :tile="false" flat nav>
        <template v-for="(p, i) in profile">
          <v-divider v-if="p.divider" :key="`divider-${i}`" class="mb-2 mt-2" />
          <app-bar-item v-else :key="`item-${i}`" @click.native="logout">
            <v-icon small left v-text="p.icon"></v-icon>
            <v-list-item-title v-text="p.title"
              ><v-icon v-text="p.icon"></v-icon
            ></v-list-item-title>
          </app-bar-item>
        </template>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
// Components
import { VHover, VListItem } from 'vuetify/lib'

// Utilities
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'DashboardCoreAppBar',

  components: {
    AppBarItem: {
      render(h) {
        return h(VHover, {
          scopedSlots: {
            default: ({ hover }) => {
              return h(
                VListItem,
                {
                  attrs: this.$attrs,
                  class: {
                    'black--text': !hover,
                    'white--text secondary elevation-12': hover,
                  },
                  props: {
                    activeClass: '',
                    dark: hover,
                    link: true,
                    ...this.$attrs,
                  },
                },
                this.$slots.default
              )
            },
          },
        })
      },
    },
  },

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },

  data: () => ({
    notifications: [
      { text: 'You have 5 new tasks', count: 12 },
      { text: "You're record approved", count: 6 },
      { text: 'Another Notification', count: 1 },
    ],
    profile: [
      { title: 'Profile', icon: 'mdi-account', action: '' },
      { title: 'Settings', icon: 'mdi-cog-outline', action: '' },
      { divider: true },
      { title: 'Log out', icon: 'mdi-logout', action: 'logout' },
    ],
  }),

  computed: {
    ...mapState(['drawer', 'user']),
  },

  created() {
    console.log(this.user)
  },

  methods: {
    ...mapMutations({
      setDrawer: 'SET_DRAWER',
    }),
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/user/login?redirect=${this.$route.fullPath}`)
    },
  },
}
</script>
