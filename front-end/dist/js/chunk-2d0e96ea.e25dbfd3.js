(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0e96ea"],{"8e07":function(t,e,n){"use strict";n.r(e);var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-app-bar",{attrs:{id:"app-bar",absolute:"",app:"",color:"transparent",flat:"",height:"75"}},[n("v-btn",{staticClass:"mr-3",attrs:{elevation:"1",fab:"",small:""},on:{click:function(e){t.$vuetify.breakpoint.smAndDown?t.setDrawer(!t.drawer):t.$emit("input",!t.value)}}},[t.value?n("v-icon",[t._v(" mdi-view-quilt ")]):n("v-icon",[t._v(" mdi-dots-vertical ")])],1),n("v-toolbar-title",{staticClass:"hidden-sm-and-down font-weight-light",domProps:{textContent:t._s(t.$t(t.$route.name))}}),n("v-spacer"),n("v-col",{attrs:{cols:"auto"}},[n("v-row",{staticClass:"font-weight-black "},[t._v("您好，"+t._s(t.user.name))])],1),n("v-col",{attrs:{cols:"auto"}},[n("v-btn",{attrs:{icon:""},on:{click:function(e){t.$vuetify.theme.dark=!t.$vuetify.theme.dark}}},[t.$vuetify.theme.dark?n("v-icon",[t._v("mdi-white-balance-sunny")]):n("v-icon",[t._v("mdi-weather-night")])],1)],1),n("v-menu",{attrs:{bottom:"",left:"","offset-y":"",origin:"top right",transition:"scale-transition"},scopedSlots:t._u([{key:"activator",fn:function(e){var r=e.attrs,o=e.on;return[n("v-btn",t._g(t._b({staticClass:"ml-2",attrs:{"min-width":"0",text:""}},"v-btn",r,!1),o),[n("v-badge",{attrs:{color:"red",overlap:"",bordered:""},scopedSlots:t._u([{key:"badge",fn:function(){return[n("span",[t._v("19")])]},proxy:!0}],null,!0)},[n("v-icon",[t._v("mdi-bell")])],1)],1)]}}])},[n("v-list",{attrs:{tile:!1,nav:""}},[n("div",t._l(t.notifications,(function(e,r){return n("app-bar-item",{key:"item-"+r},[n("v-list-item-title",[n("v-badge",{staticClass:"mr-3",attrs:{color:"red",overlap:"",bordered:""},scopedSlots:t._u([{key:"badge",fn:function(){return[n("span",[t._v(t._s(e.count))])]},proxy:!0}],null,!0)},[n("v-icon",{attrs:{left:""}},[t._v("mdi-bell")])],1),t._v(" "+t._s(e.text)+" ")],1)],1)})),1)])],1),n("v-menu",{attrs:{bottom:"",left:"","min-width":"200","offset-y":"",origin:"top right",transition:"scale-transition"},scopedSlots:t._u([{key:"activator",fn:function(e){var r=e.attrs,o=e.on;return[n("v-btn",t._g(t._b({staticClass:"ml-2",attrs:{"min-width":"0",text:""}},"v-btn",r,!1),o),[n("v-icon",{attrs:{left:""}},[t._v("mdi-account")])],1)]}}])},[n("v-list",{attrs:{tile:!1,flat:"",nav:""}},[t._l(t.profile,(function(e,r){return[e.divider?n("v-divider",{key:"divider-"+r,staticClass:"mb-2 mt-2"}):n("app-bar-item",{key:"item-"+r,nativeOn:{click:function(e){return t.logout(e)}}},[n("v-icon",{attrs:{small:"",left:""},domProps:{textContent:t._s(e.icon)}}),n("v-list-item-title",{domProps:{textContent:t._s(e.title)}},[n("v-icon",{domProps:{textContent:t._s(e.icon)}})],1)],1)]}))],2)],1)],1)},o=[],a=(n("a4d3"),n("4de4"),n("4160"),n("e439"),n("dbb4"),n("b64b"),n("159b"),n("96cf"),n("1da1")),i=n("ade3"),s=n("ce87"),c=n("da13"),l=n("2f62");function u(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,r)}return n}function d(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?u(Object(n),!0).forEach((function(e){Object(i["a"])(t,e,n[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):u(Object(n)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))}))}return t}var v={name:"DashboardCoreAppBar",components:{AppBarItem:{render:function(t){var e=this;return t(s["a"],{scopedSlots:{default:function(n){var r=n.hover;return t(c["a"],{attrs:e.$attrs,class:{"black--text":!r,"white--text secondary elevation-12":r},props:d({activeClass:"",dark:r,link:!0},e.$attrs)},e.$slots.default)}}})}}},props:{value:{type:Boolean,default:!1}},data:function(){return{notifications:[{text:"You have 5 new tasks",count:12},{text:"You're record approved",count:6},{text:"Another Notification",count:1}],profile:[{title:"Profile",icon:"mdi-account",action:""},{title:"Settings",icon:"mdi-cog-outline",action:""},{divider:!0},{title:"Log out",icon:"mdi-logout",action:"logout"}]}},computed:d({},Object(l["c"])(["drawer","user"])),created:function(){console.log(this.user)},methods:d({},Object(l["b"])({setDrawer:"SET_DRAWER"}),{logout:function(){var t=Object(a["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,this.$store.dispatch("user/logout");case 2:this.$router.push("/user/login?redirect=".concat(this.$route.fullPath));case 3:case"end":return t.stop()}}),t,this)})));function e(){return t.apply(this,arguments)}return e}()})},p=v,f=n("2877"),b=n("6544"),m=n.n(b),h=n("40dc"),g=n("4ca6"),w=n("8336"),_=n("62ad"),y=n("ce7e"),k=n("132d"),O=n("8860"),x=n("5d23"),j=n("e449"),C=n("0fd9"),P=n("2fa4"),$=n("2a7f"),V=Object(f["a"])(p,r,o,!1,null,null,null);e["default"]=V.exports;m()(V,{VAppBar:h["a"],VBadge:g["a"],VBtn:w["a"],VCol:_["a"],VDivider:y["a"],VIcon:k["a"],VList:O["a"],VListItemTitle:x["k"],VMenu:j["a"],VRow:C["a"],VSpacer:P["a"],VToolbarTitle:$["c"]})}}]);
//# sourceMappingURL=chunk-2d0e96ea.e25dbfd3.js.map