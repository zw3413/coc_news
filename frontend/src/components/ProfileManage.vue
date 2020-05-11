<template>
  <div style>
    <div style="margin:10px 200px">
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="模板名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="模板标题">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="索引页链接">
          <el-input v-model="form.firstPage"></el-input>
        </el-form-item>
        <el-form-item label="链接选择器">
          <el-input v-model="form.urlSelector"></el-input>
        </el-form-item>
        <el-form-item label="标题选择器">
          <el-input v-model="form.titleSelector"></el-input>
        </el-form-item>
        <el-form-item label="作者选择器">
          <el-input v-model="form.authorSelector"></el-input>
        </el-form-item>
        <el-form-item label="正文选择器">
          <el-input v-model="form.contentSelector"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit">保存</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-table :data="list" style="width: 100%; bottom:0px" border>
      <el-table-column prop="name" label="模板名称"></el-table-column>
      <el-table-column prop="title" label="模板标题"></el-table-column>
      <el-table-column prop="firstPage" label="索引页链接"></el-table-column>
      <el-table-column prop="urlSelector" label="链接选择器"></el-table-column>
      <el-table-column prop="titleSelector" label="标题选择器"></el-table-column>
      <el-table-column prop="authorSelector" label="作者选择器"></el-table-column>
      <el-table-column prop="contentSelector" label="正文选择器"></el-table-column>
      <el-table-column prop="rss_url" label="RSS"></el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button @click="edit(scope.row)" type="text" size="small">编辑</el-button>
          <el-button @click="deleteItem(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import {getList} from '../api/profile'
export default {
  data() {
    return {
      list: [],
      form: {
        name: "",
        title: "",
        firstPage: "",
        urlSelector: "",
        titleSelector: "",
        authorSelector: "",
        contentSelector: "",
        rss_url:""
      }
    };
  },
  methods: {
    deleteItem(row) {
      var name = row.name;
      fetch("http://192.168.31.144:8000/deleteProfile?name=" + name)
        .then(resp => resp.text())
        .then(json => {
          var result = JSON.parse(json);
          if (result.code == "200") {
            alert("删除成功");
            this.fetchList();
          } else {
            alert("删除失败");
          }
        });
    },
    edit(row) {
      this.form = {
        name: row.name,
        title: row.title,
        firstPage: row.firstPage,
        urlSelector: row.urlSelector,
        titleSelector: row.titleSelector,
        authorSelector: row.authorSelector,
        contentSelector: row.contentSelector,
        rss_url:row.rss_url
      };
    },
    fetchList() {
      this.list = [];
      getList()
        .then(result => {
          //console.log(result)
          //var data = JSON.parse(result);
          var data=result
          for (var i in data) {
            var val = data[i];
            var obj = {
              name: val.name,
              title: val.title,
              firstPage: val.first_page,
              urlSelector: val.url_selector,
              titleSelector: val.title_selector,
              authorSelector: val.author_selector,
              contentSelector: val.content_selector,
              rss_url:val.rss_url
            };
            this.list.push(obj);
          }
        });
    },
    onSubmit() {
      fetch(
        "http://192.168.31.144:8000/saveProfile?" + this.urlEncode(this.form)
      )
        .then(resp => resp.text())
        .then(json => {
          var result = JSON.parse(json);
          if (result.code == "200") {
            this.form = {
              name: "",
              title: "",
              firstPage: "",
              urlSelector: "",
              titleSelector: "",
              authorSelector: "",
              contentSelector: ""
            };
            this.fetchList();
          } else {
            alert("保存失败");
          }
        });
    },
    urlEncode: function(param, key, encode) {
      if (param == null) return "";
      var paramStr = "";
      var t = typeof param;
      if (t == "string" || t == "number" || t == "boolean") {
        paramStr +=
          "&" +
          key +
          "=" +
          (encode == null || encode ? encodeURIComponent(param) : param);
      } else {
        for (var i in param) {
          var k =
            key == null
              ? i
              : key + (param instanceof Array ? "[" + i + "]" : "." + i);
          paramStr += this.urlEncode(param[i], k, encode);
        }
      }
      return paramStr;
    }
  },
  mounted: function() {
    this.fetchList();
  }
};
</script>
<style scoped>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>