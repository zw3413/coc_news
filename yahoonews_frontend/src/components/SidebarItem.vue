<template>
  <div>
    <el-menu-item ref="subMenu" :index="item.path" popper-append-to-body>
      <i :class="item.meta && item.meta.icon"/>
      <router-link
        :to="item.path"
      >{{item.meta.title}}</router-link>
    </el-menu-item>
  </div>
</template>

<script>
import FixiOSBug from "./FixiOSBug";

export default {
  name: "SidebarItem",
  mixins: [FixiOSBug],
  props: {
    // route object
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ""
    }
  },
  data() {
    // To fix https://github.com/PanJiaChen/vue-admin-template/issues/237
    // TODO: refactor with render function
    this.onlyOneChild = null;
    return {};
  },
  methods: {
   
  }
};
</script>
