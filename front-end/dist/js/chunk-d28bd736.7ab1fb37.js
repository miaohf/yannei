(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-d28bd736"],{"0348":function(t,e,i){},"126f":function(t,e,i){"use strict";i.r(e);var s=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("v-container",{staticClass:"px-4 py-0",attrs:{fluid:""},scopedSlots:t._u([{key:"after-heading",fn:function(){},proxy:!0}])},[i("v-card",{staticClass:"pt-6"},[i("div",{staticClass:"px-10 pb-5",attrs:{height:"800px"}},[i("v-row",[i("v-col",{attrs:{cols:"12",md:"7"}},[i("v-row",[i("v-col",{attrs:{cols:"12",md:"8"}},[i("v-text-field",{attrs:{color:"yellow darken-3",label:"客户名称",hint:"",required:"",disabled:"","prepend-icon":"mdi-account-group"},model:{value:t.temp.visit.customer_name,callback:function(e){t.$set(t.temp.visit,"customer_name",e)},expression:"temp.visit.customer_name"}})],1),i("v-col",{attrs:{cols:"12",md:"2"}},[i("v-autocomplete",{attrs:{items:t.visittypes,"item-text":"name","item-value":"id",label:"拜访类型",placeholder:"","prepend-icon":"mdi-alpha-t-circle",disabled:""},model:{value:t.temp.visit.visittype_id,callback:function(e){t.$set(t.temp.visit,"visittype_id",e)},expression:"temp.visit.visittype_id"}})],1),i("v-col",{attrs:{cols:"12",md:"2"}},[i("v-autocomplete",{attrs:{items:t.statusCodes,"item-text":"display_name","item-value":"key",label:"状态",placeholder:"","prepend-icon":"mdi-alpha-s-box",disabled:""},model:{value:t.temp.status_code,callback:function(e){t.$set(t.temp,"status_code",e)},expression:"temp.status_code"}})],1)],1),i("v-row",[i("v-col",{attrs:{cols:"12",md:"7"}},[i("v-row",[i("v-col",{attrs:{cols:"12",md:"8"}},[i("v-text-field",{attrs:{color:"yellow darken-3",label:"档案编号",hint:"",required:"",disabled:"","prepend-icon":"mdi-file"},model:{value:t.temp.document_code,callback:function(e){t.$set(t.temp,"document_code",e)},expression:"temp.document_code"}})],1)],1)],1)],1),i("v-row",[i("v-col",[i("v-autocomplete",{attrs:{items:t.contactors,"item-text":"name","item-value":"id",label:"联系人",placeholder:"本次拜访接待人员","prepend-icon":"mdi-account-search-outline",multiple:"",chips:"",disabled:""},model:{value:t.temp.visit.contactorids,callback:function(e){t.$set(t.temp.visit,"contactorids",e)},expression:"temp.visit.contactorids"}})],1)],1),i("v-row",[i("v-col",[i("v-autocomplete",{attrs:{items:t.addresses,"item-text":"name","item-value":"id",label:"拜访地址",placeholder:"","prepend-icon":"mdi-alpha-t-circle",disabled:""},model:{value:t.temp.visit.address_id,callback:function(e){t.$set(t.temp.visit,"address_id",e)},expression:"temp.visit.address_id"}})],1)],1),i("v-divider",{staticClass:"mt-12"}),i("v-row",[i("v-col",{attrs:{cols:"12",md:"8"}},[i("v-text-field",{attrs:{color:"yellow darken-3",label:"标题",hint:"简述此次拜访目的",required:"","prepend-icon":"mdi-subtitles",disabled:""},model:{value:t.temp.visit.title,callback:function(e){t.$set(t.temp.visit,"title",e)},expression:"temp.visit.title"}})],1),i("v-col",{attrs:{cols:"12",md:"4"}},[i("v-text-field",{attrs:{color:"yellow darken-3",label:"创建者",required:"",disabled:"","prepend-icon":"mdi-account"},model:{value:t.temp.visit.author.name,callback:function(e){t.$set(t.temp.visit.author,"name",e)},expression:"temp.visit.author.name"}})],1)],1)],1),i("v-col",{attrs:{cols:"12",md:"5"}},[i("v-carousel",{attrs:{cycle:"",height:"300","show-arrows-on-hover":"","delimiter-icon":"mdi-minus"}},t._l(t.temp.visit.attachments,(function(t,e){return i("v-carousel-item",{key:e},[i("v-row",{staticClass:"fill-height",attrs:{align:"center",justify:"center"}},[i("v-img",{attrs:{"max-height":"600",src:t.uri}})],1)],1)})),1)],1)],1),i("v-textarea",{attrs:{color:"yellow darken-3",label:"描述拜访经过和成果",hint:"",required:"","prepend-icon":"mdi-content-copy","auto-grow":"",disabled:""},model:{value:t.temp.visit.description,callback:function(e){t.$set(t.temp.visit,"description",e)},expression:"temp.visit.description"}})],1),i("div",{staticClass:"px-10 pb-5",attrs:{height:"800px"}},[i("v-timeline",{attrs:{"align-top":"",dense:t.$vuetify.breakpoint.smAndDown}},t._l(t.temp.orderrecs,(function(e,s){return i("v-timeline-item",{key:s,attrs:{"fill-dot":"",color:t.colors[s]}},[i("v-card",{attrs:{color:t.colors[s],dark:""}},[i("v-card-title",{staticClass:"text-h6"},[t._v(" "+t._s(s+1)+". "+t._s(e.nodename)+"status_code:"+t._s(e.status_code)+" ")]),i("v-card-text",{staticClass:"white text--primary"},[i("p",[t._v(" "+t._s(e.team.team_member)+" ")]),i("p",[t._v(" "+t._s(e.opinion_text)+" ")]),t.canAudit(e.team.team_member)&&0===e.status_code?i("div",[i("add-audit-dialog",{attrs:{"orderrec-id":e.id}})],1):t._e()])],1)],1)})),1)],1)])],1)},a=[],n=(i("4160"),i("caad"),i("d81d"),i("4e827"),i("d3b7"),i("2532"),i("159b"),i("b30f")),o=i("8024"),r=[{key:0,display_name:"新建"},{key:1,display_name:"提审"},{key:2,display_name:"完成"},{key:3,display_name:"通过"},{key:9,display_name:"驳回"}],c={name:"OrderDetails",components:{AddAuditDialog:function(){return i.e("chunk-2d214078").then(i.bind(null,"aeca"))}},filters:{statusFilter:function(t){var e={published:"success",draft:"info",deleted:"danger"};return e[t]}},data:function(){return{statusCodes:r,listLoading:!1,contactors:[],addresses:[],visittypes:[],details:null,temp:{attachments:[],visit:{author:{}}},rules:{},users:[],colors:["#0099CC","#FF6666","#FFCCCC","#0099CC","#FF6666","#FFCCCC"]}},computed:{isAdminRole:function(){return"administrator"===this.$store.getters.role.slug}},created:function(){this.fetchData(),this.getVisittypesList()},methods:{goBack:function(){this.$router.go(-1)},canAudit:function(t){var e=this.$store.getters.userId;return t.map((function(t){return t.id})).includes(e)},isAuthor:function(t){var e=this.$store.getters.userId;return e===t},fetchData:function(){var t=this;this.listLoading=!0;var e=this.$route.params&&this.$route.params.id;Object(n["a"])(e).then((function(e){t.temp=e.data,t.getContactorsListbyCustomerId(t.temp.visit.customer_id),t.getAddressesListbyCustomerId(t.temp.visit.customer_id),setTimeout((function(){t.listLoading=!1}),5e3)}))},getContactorsListbyCustomerId:function(t){var e=this;Object(o["c"])(t).then((function(t){e.contactors=t.data.items,setTimeout((function(){e.listLoading=!1}),1500)}))},getAddressesListbyCustomerId:function(t){var e=this;Object(o["a"])(t).then((function(t){e.addresses=t.data.items,setTimeout((function(){e.listLoading=!1}),1500)}))},editOrder:function(){var t=this;this.listLoading=!0;var e=this.$route.params&&this.$route.params.id;Object(n["c"])(e,this.temp).then((function(e){t.temp=e.data,setTimeout((function(){t.listLoading=!1}),5e3)}))},getVisittypesList:function(){var t=this;Object(o["f"])().then((function(e){t.visittypes=e.data.items,setTimeout((function(){t.listLoading=!1}),1500)}))},getNamefromOptions:function(t,e){var i="";return t.forEach((function(t){t.key===e&&(i=t.display_name)})),i},getSortClass:function(t){var e=this.listQuery.sort;return e==="+".concat(t)?"ascending":"descending"}}},d=c,l=(i("c4b2"),i("2877")),u=i("6544"),m=i.n(u),p=i("c6a6"),v=i("b0af"),f=i("99d9"),h=i("5e66"),b=i("3e35"),g=i("62ad"),_=i("a523"),y=i("ce7e"),C=i("adda"),x=i("0fd9"),k=i("8654"),w=i("a844"),$=i("8414"),O=i("1e06"),V=Object(l["a"])(d,s,a,!1,null,"603124be",null);e["default"]=V.exports;m()(V,{VAutocomplete:p["a"],VCard:v["a"],VCardText:f["d"],VCardTitle:f["e"],VCarousel:h["a"],VCarouselItem:b["a"],VCol:g["a"],VContainer:_["a"],VDivider:y["a"],VImg:C["a"],VRow:x["a"],VTextField:k["a"],VTextarea:w["a"],VTimeline:$["a"],VTimelineItem:O["a"]})},8024:function(t,e,i){"use strict";i.d(e,"e",(function(){return a})),i.d(e,"b",(function(){return n})),i.d(e,"d",(function(){return o})),i.d(e,"c",(function(){return r})),i.d(e,"a",(function(){return c})),i.d(e,"f",(function(){return d}));var s=i("b775");function a(){return Object(s["a"])({url:"/selections/provinces",method:"get"})}function n(t){return Object(s["a"])({url:"/selections/cities/".concat(t),method:"get"})}function o(){return Object(s["a"])({url:"/selections/customers",method:"get"})}function r(t){return Object(s["a"])({url:"/selections/contactors/".concat(t),method:"get"})}function c(t){return Object(s["a"])({url:"/selections/addresses/".concat(t),method:"get"})}function d(){return Object(s["a"])({url:"/selections/visittypes",method:"get"})}},b30f:function(t,e,i){"use strict";i.d(e,"b",(function(){return a})),i.d(e,"a",(function(){return n})),i.d(e,"c",(function(){return o}));var s=i("b775");function a(t){return Object(s["a"])({url:"/orders",method:"get",params:t})}function n(t){return Object(s["a"])({url:"/orders/".concat(t),method:"get"})}function o(t,e){return Object(s["a"])({url:"/orders/".concat(t),method:"put",data:e})}},c4b2:function(t,e,i){"use strict";var s=i("0348"),a=i.n(s);a.a}}]);
//# sourceMappingURL=chunk-d28bd736.7ab1fb37.js.map