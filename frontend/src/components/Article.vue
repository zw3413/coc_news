<template>
  <div style>
  <div style="width:100%;height:20px;text-align:center">
      <p><a href="#" @click="loadNextPage()">load more</a></p>
    </div>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="media_content" label="media_content" width="200px">
        <template slot-scope="scope">
          <ul>
            <li v-for="media in scope.row.media_content" :key="media.url">
              <img
                :src="media.url"
                :height="media.height"
                :width="media.width"
                :alt="scope.row.media_text"
              />
            </li>
          </ul>
          <!-- <p v-html="scope.row.media_content"></p> -->
        </template>
      </el-table-column>
      <!-- <el-table-column label="id">
        <template slot-scope="scope">
          <span :title="scope.row.guid">{{scope.row.id}}</span>
        </template>
      </el-table-column>-->
      <el-table-column label="title">
        <template slot-scope="scope">
          <p>
            {{scope.row.title}}
            &nbsp;&nbsp;&nbsp;&nbsp;
            <a
              v-if="scope.row.content && scope.row.content != ''"
              @click="showArticle(scope.row)"
            >正文</a>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <a v-bind:href="scope.row.link" v-bind:title="scope.row.link" target="_blank">原文链接</a>
          </p>
          <p>
            <span>{{scope.row.pub_date}}</span>
          </p>
          <p>
            <a
              :href="scope.row.source_url"
              :title="scope.row.source_url"
              target="_blank"
            >{{scope.row.source}}</a>
          </p>
        </template>
      </el-table-column>
      <!-- <el-table-column prop="summary" label="summary"></el-table-column>
      <el-table-column prop="description" label="description"></el-table-column>-->
      <!-- <el-table-column prop="link" label="link"></el-table-column> -->
      <!-- <el-table-column prop="pub_date" label="pub_date"></el-table-column> -->
      <!-- <el-table-column prop="source" label="source">
        <template slot-scope="scope">
          <a
            :href="scope.row.source_url"
            :title="scope.row.source_url"
            target="_blank"
          >{{scope.row.source}}</a>
        </template>
      </el-table-column>-->
      <!-- <el-table-column prop="source_url" label="source_url"></el-table-column> -->
      <!-- <el-table-column prop="guid" label="guid"></el-table-column> -->

      <!-- <el-table-column prop="media_text" label="media_text"></el-table-column> -->
      <!-- <el-table-column prop="profile_name" label="profile_name"></el-table-column> -->
      <!-- <el-table-column prop="update_time" label="update_time"></el-table-column> -->
    </el-table>
    
    <el-dialog 
    title="正文" 
    :visible.sync="dialogVisible"  
    width="90%"
  
    >
      <h2 v-html="article.title"></h2>
      <div v-html="article.content"></div>
      <ul >
        <li v-for="translation in translations" :key="translation.guid">
          <span v-html="translation.type"></span>
          <h2 v-html="translation.title"></h2>
          <div v-html="translation.content"></div>
        <li>
      <ul>
      <!-- <div slot="footer" class="dialog-footer">
        <el-button @click.native="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="addLoading">提交</el-button>
      </div> -->
    </el-dialog>
  </div>
</template>
<script>
//import {urlEncode} from '../utils/common_util'
import { getList } from "../api/article";
import {getTranslationByGuid} from "../api/article";
export default {
  data() {
    return {
      article:{},
      translations:{},
      params: {page:0},
      tableData: [],
      dialogVisible: false, //模态框是否显示
      addLoading: false //是否显示loading
    };
  },
  methods: {
    loadNextPage:function() {
      this.fetchList()
    },
    opendialog: function() {
      //代开模态框
      this.dialogVisible = false;
    },
    fetchList: function() {
      this.params.page++;
      getList(this.params).then(data => {
        if(typeof(data.results) =="undefined" ){
            alert('没有更多的内容')
        }else{
        //console.log(data)
        data.results.forEach(function(v) {
          //v.title=url
          v.media_content = eval(v.media_content);    
          if (v.media_content) {
            v.media_content.forEach(c => {
              if (typeof c.width == "undefined") c.width = "130";
              if (typeof c.height == "undefined") c.height = "90";
            });
          }
        });
        this.tableData = data.results.concat(this.tableData);
        console.log(this.tableData)
        }
      });
    },
    showArticle: function(row) {

      this.article=row

      getTranslationByGuid({guid:row.guid}).then(data=>{
        //  if(typeof(data.results) =="undefined" ){
        //     alert('没有更多的内容')
        // }else{   
        //   this.translations = data.results;
        //   console.log(this.tableData)
        // }
        this.translations=data;
        console.log(this.translations)
      })

      this.dialogVisible=true
      // this.$alert(content, "正文", {
      //   dangerouslyUseHTMLString: true,
      //   center: true,
      //   customClass: "article-content",
      //   showConfirmButton: false
      // });
    }
  },
  computed: {},
  mounted: function() {
    this.fetchList();
  }
};
</script>
<style>
li {
  list-style-type: none;
}
.article-content {
  width: 90% !important;
}
div {
  padding:0 !important;
}
.el-dialog button{
  display:none
}
</style>