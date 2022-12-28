(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d21d0d1"],{d03b:function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-dialog",{attrs:{"max-width":"1200"},scopedSlots:e._u([{key:"activator",fn:function(t){var l=t.on,s=t.attrs;return[a("v-btn",e._g(e._b({staticClass:"mx-1 my-2",attrs:{text:"",small:"",color:"primary"}},"v-btn",s,!1),l),[a("v-icon",[e._v("mdi-plus")])],1)]}}]),model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[a("v-container",[a("v-card",[a("div",{staticClass:"px-7 pb-5",attrs:{height:"800px"}},[a("v-card-title",{staticClass:"my-6"},[a("h1",[e._v("新增客户联系人")])]),a("v-subheader",{staticClass:"mx-2"},[e._v("基本信息")]),a("v-row",[a("v-col",{attrs:{cols:"12",sm:"3",md:"3"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"姓名",hint:"填写客户联系人姓名",required:""},model:{value:e.temp.name,callback:function(t){e.$set(e.temp,"name",t)},expression:"temp.name"}})],1),a("v-col",{attrs:{cols:"12",sm:"1",md:"1"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"年龄",hint:"",required:""},model:{value:e.temp.age,callback:function(t){e.$set(e.temp,"age",t)},expression:"temp.age"}})],1),a("v-col",{attrs:{cols:"12",sm:"2",md:"2"}},[a("v-select",{staticClass:"mx-6",attrs:{items:e.sexOptions,"item-text":"display_name","item-value":"key","menu-props":"auto","hide-details":"",label:"性别","single-line":""},model:{value:e.temp.sex,callback:function(t){e.$set(e.temp,"sex",t)},expression:"temp.sex"}})],1),a("v-col",{attrs:{cols:"12",sm:"2",md:"2"}},[a("v-select",{staticClass:"mx-6",attrs:{items:e.educationLevels,"item-text":"display_name","item-value":"key","menu-props":"auto","hide-details":"",label:"教育","single-line":""},model:{value:e.temp.education_level,callback:function(t){e.$set(e.temp,"education_level",t)},expression:"temp.education_level"}})],1),a("v-col",{attrs:{cols:"12",sm:"4",md:"4"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"职位描述",hint:"填写受访者当前职务后者项目中的角色",required:""},model:{value:e.temp.position,callback:function(t){e.$set(e.temp,"position",t)},expression:"temp.position"}})],1)],1),a("v-subheader",{staticClass:"mx-2"},[e._v("联系资料")]),a("v-row",[a("v-col",{attrs:{cols:"12",sm:"2",md:"2"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"移动电话",hint:"填写联系人个人移动电话号码",required:""},model:{value:e.temp.mobile,callback:function(t){e.$set(e.temp,"mobile",t)},expression:"temp.mobile"}})],1),a("v-col",{attrs:{cols:"12",sm:"2",md:"2"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"固定电话",hint:"填写联系人办公固话号码",required:""},model:{value:e.temp.phone,callback:function(t){e.$set(e.temp,"phone",t)},expression:"temp.phone"}})],1),a("v-col",{attrs:{cols:"12",sm:"2",md:"2"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"微信",hint:"填写客户微信号或者微信绑定的手机号",required:""},model:{value:e.temp.weichatid,callback:function(t){e.$set(e.temp,"weichatid",t)},expression:"temp.weichatid"}})],1),a("v-col",{attrs:{cols:"12",sm:"3",md:"3"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"邮箱地址",hint:"填写邮箱地址",required:""},model:{value:e.temp.email,callback:function(t){e.$set(e.temp,"email",t)},expression:"temp.email"}})],1),a("v-col",{attrs:{cols:"12",sm:"3",md:"3"}},[a("v-text-field",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"办公地址",hint:"填写办公室所在楼幢、楼层、门牌号等",required:""},model:{value:e.temp.office_address,callback:function(t){e.$set(e.temp,"office_address",t)},expression:"temp.office_address"}})],1)],1),a("v-expansion-panels",{attrs:{accordion:""}},[a("v-expansion-panel",[a("v-expansion-panel-header",[e._v("其他信息")]),a("v-expansion-panel-content",[a("v-row",[a("v-col",[a("v-textarea",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"毕业情况（选填）",hint:"填写联系人毕业院校、毕业年份等信息",required:""},model:{value:e.temp.graduated_school,callback:function(t){e.$set(e.temp,"graduated_school",t)},expression:"temp.graduated_school"}})],1)],1),a("v-row",[a("v-col",[a("v-textarea",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"配偶情况（选填）",hint:"填写联系人配偶教育、工作等信息",required:""},model:{value:e.temp.spouse_detail,callback:function(t){e.$set(e.temp,"spouse_detail",t)},expression:"temp.spouse_detail"}}),a("v-textarea",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"子女情况（选填）",hint:"填写联系人子女教育、工作相关情况",required:""},model:{value:e.temp.child_detail,callback:function(t){e.$set(e.temp,"child_detail",t)},expression:"temp.child_detail"}})],1)],1),a("v-row",[a("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[a("v-textarea",{staticClass:"mx-6",attrs:{color:"yellow darken-3",label:"其他备注（选填）",hint:"填写联系人其他信息",required:""},model:{value:e.temp.description,callback:function(t){e.$set(e.temp,"description",t)},expression:"temp.description"}})],1)],1)],1)],1)],1),a("v-row",[a("v-spacer"),a("span",{staticClass:"mt-6 mx-3 orange--text",staticStyle:{"font-size":"14px"}},[e._v(" 本系统由 研一智控 提供技术支持。 ")])],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"warning"},on:{click:e.cancelAddDialog}},[e._v("取消")]),a("v-btn",{attrs:{color:"primary",disabled:0===e.temp.name.length},on:{click:e.confirmAddDialog}},[e._v("确认")])],1)],1)])],1)],1)},s=[],o=a("9671"),i=[{key:1,display_name:"高中"},{key:2,display_name:"中专"},{key:3,display_name:"大专"},{key:4,display_name:"本科"},{key:5,display_name:"硕士"},{key:6,display_name:"博士"},{key:7,display_name:"教授"}],n=[{key:0,display_name:"男"},{key:1,display_name:"女"}],c={name:"AddCustomerDialog",components:{},data:function(){return{educationLevels:i,sexOptions:n,provinces:[],cities:[],dialog:!1,temp:{type:"contactor",name:"",description:"",phone:""}}},mounted:function(){},created:function(){},methods:{confirmAddDialog:function(){var e=this,t=this.$route.params.id,a=this.temp;Object(o["a"])(t,a).then((function(){e.dialog=!1,e.temp={type:"contactor",name:""},e.$emit("fetchData")}))},cancelAddDialog:function(){this.dialog=!1,this.temp={type:"contactor",name:""}}}},r=c,d=a("2877"),m=a("6544"),p=a.n(m),v=a("8336"),u=a("b0af"),x=a("99d9"),b=a("62ad"),f=a("a523"),h=a("169a"),k=a("cd55"),y=a("49e2"),_=a("c865"),w=a("0393"),C=a("132d"),g=a("0fd9"),V=a("b974"),$=a("2fa4"),q=a("e0c7"),D=a("8654"),A=a("a844"),E=Object(d["a"])(r,l,s,!1,null,"7462b68b",null);t["default"]=E.exports;p()(E,{VBtn:v["a"],VCard:u["a"],VCardActions:x["b"],VCardTitle:x["e"],VCol:b["a"],VContainer:f["a"],VDialog:h["a"],VExpansionPanel:k["a"],VExpansionPanelContent:y["a"],VExpansionPanelHeader:_["a"],VExpansionPanels:w["a"],VIcon:C["a"],VRow:g["a"],VSelect:V["a"],VSpacer:$["a"],VSubheader:q["a"],VTextField:D["a"],VTextarea:A["a"]})}}]);
//# sourceMappingURL=chunk-2d21d0d1.be5dcd55.js.map