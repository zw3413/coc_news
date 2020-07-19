<template>
  <el-upload
    ref="upload"
    drag
    :auto-upload="true"
    :http-request="uploadSectionFile"
    action="fakeAction"
    :limit="1"
  >
    <i class="el-icon-upload"></i>
    <div class="el-upload__text">
      将文件拖到此处，或
      <em>点击上传</em>
    </div>
  </el-upload>
</template>
<script>
export default {
  data() {
    return {};
  },
  methods: {
    uploadSectionFile: function(params) {
      var self = this;
      var file = params.file;
      // fileType = file.type,
      // file_url = self.$refs.upload.uploadFiles[0].url;

      //http://cloudbed.cn/#/admin/videotoole
      //http://cloudbed.cn/#/admin/upload/mp3
      //视频上传
      self.upload_url = "http://cloudbed.cn:8000/upload/mp3";
      //self.upload_url = "http://127.0.0.1:8000/upload/mp3";
      self.upload_name = "file";
      self.uploadFile(file);
    },

    uploadFile: function(file) {
      var self = this;
      var formData = new FormData();
      formData.append(self.upload_name, file);
      self.$axios
        .post(self.upload_url, formData, {
          headers: { "Content-Type": "multipart/form-data" }
        })
        .then(function(res) {
          alert(res);
        });
    }
  }
};
</script>
<style scoped>
</style>