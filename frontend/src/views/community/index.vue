<template>
  <div class="app-container">
    <!-- 上传一个压缩包数据集按钮 -->
    <div class="button-group-item">
      <el-upload
        class="upload-dataset"
        accept="application/x-zip-compressed"
        action="http://localhost:8000/api/community/uploadDataset/"
        name="dataset_zip"
        :headers="{ 'annotate-system-token': token }"
        :limit="1"
        :on-exceed="handleExceed"
        :before-upload="handleBeforeZipUpload"
        :on-success="handleSuccess"
        :on-error="handleError"
        multiple
      >
        <el-button type="primary" size="small" icon="el-icon-upload2">
          上传数据集
        </el-button>
        <div slot="tip" class="el-upload__tip">
          只能上传.zip文件，可以包含jpg/png/mp4，且不超过20M
        </div>
      </el-upload>
    </div>
    <div class="clear">
      <el-button
        type="danger"
        size="small"
        icon="el-icon-delete"
        @click="removeAll"
      >
        清空
      </el-button>
    </div>
    <!-- 搜索框 -->
    <div class="search">
      <el-input
        v-model="keywords"
        placeholder="请搜索关键词"
        class="input-with-select"
        @input="search"
      >
        <el-select slot="prepend" v-model="searchTarget">
          <el-option label="描述" value="description"></el-option>
          <el-option label="数据集名" value="text"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="search" />
      </el-input>
    </div>

    <!-- 表格 -->
    <div>
      <el-table
        v-loading="listLoading"
        :data="filterList"
        element-loading-text="Loading"
        :row-class-name="tableRowClassName"
        size="mini"
        border
        fit
      >
        <!-- 序号 -->
        <el-table-column align="center" label="序号" width="50">
          <template slot-scope="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <!-- 数据集信息 -->
        <el-table-column label="数据集名" align="center">
          <template slot-scope="scope">
            <p class="single-line">
              {{ scope.row.name }}
            </p>
          </template>
        </el-table-column>
        <!-- 描述 -->
        <el-table-column label="描述" align="center">
          <template slot-scope="scope">
            <p class="single-line">
              {{ scope.row.description }}
            </p>
          </template>
        </el-table-column>
        <!-- 发布者 -->
        <el-table-column label="发布者" width="180" align="center">
          <template slot-scope="scope"
            ><p class="single-line">
              {{ scope.row.publisher }}
            </p>
          </template>
        </el-table-column>
        <!-- 图片数量 -->
        <el-table-column label="图片数量" width="130" align="center">
          <template slot-scope="scope"
            ><p class="single-line">
              {{ scope.row.num }}
            </p>
          </template>
        </el-table-column>
        <!-- 状态 -->
        <el-table-column
          class-name="status-col"
          label="状态"
          width="110"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.status | statusFilter">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <!-- 操作 -->
        <el-table-column label="操作" width="220" align="center">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="addToMyDataset(scope.$index)"
            >
              领取
            </el-button>
            <el-button
              size="mini"
              type="success"
              @click="handleEdit(scope.$index, scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 编辑框 -->
    <el-dialog :visible.sync="showEditForm" :width="width">
      <el-form label-position="left" label-width="80px" :model="form">
        <el-form-item label="描述">
          <el-input v-model="form.description"></el-input>
        </el-form-item>
        <el-form-item label="数据集名">
          <el-input
            v-model="form.name"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 5 }"
            placeholder="请输入内容"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="update"> 更新 </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getCommunityInfoApi,
  deleteCommunityDatasetApi,
  removeAllCommunityDatasetApi,
  updateCommunityDatasetInfoApi,
} from "@/api/community";
import { addAnnotatedSetApi } from "@/api/myDataset";
import { getToken } from "@/utils/auth";
import { mapGetters } from "vuex";

export default {
  name: "CommunityTableList",
  filters: {
    statusFilter(status) {
      const statusMap = {
        有人认领: "success",
        无人认领: "gray",
      };
      return statusMap[status];
    },
  },

  data() {
    return {
      searchTarget: "描述", // 搜索对象

      keywords: "", // 搜索关键词
      filterList: [], //符合条件的数据
      list: [], // 所有数据列表
      listLoading: true, //加载效果
      showEditForm: false, //编辑框的显隐
      listEditIndex: 0, // 编辑索引
      handleItemId: 0, // 操作条目的id
      form: {
        //编辑框数据
        description: "",
        name: "",
      },
    };
  },
  computed: {
    // 编辑框宽度
    width() {
      return window.innerWidth <= 400 ? "80%" : "30%";
    },
    token() {
      return getToken();
    },
    ...mapGetters(["communityDatasetList"]),
  },
  created() {
    // 获取数据社区信息
    getCommunityInfoApi().then((res) => {
      this.$store.dispatch("community/setDatasetList", res.data.dataset_list);
      this.list = this.filterList = this.communityDatasetList;
      this.listLoading = false;
    });
  },
  mounted() {
    this.list = this.filterList = this.communityDatasetList;
    this.listLoading = false;
  },
  methods: {
    /**
     * 上传zip数据集压缩包
     */
    handleBeforeZipUpload(file) {
      // TODO:检查压缩包格式，以后还可以增加直接上传图片、视频等
      const fileType = file.type;
      const fileSize = file.size;
      if (fileType === "application/x-zip-compressed") {
        if (fileSize / 1024 / 1024 / 20 > 1) {
          this.$message.error("文件大小不能超过20M");
          return false;
        }
        return true;
      } else {
        this.$message.error("仅支持上传.zip压缩包文件");
        return false;
      }
    },
    handleSuccess(response) {
      this.$store.dispatch(
        "community/addNewDataset",
        response.data.new_dataset_info
      );
      this.$message.success("上传成功");
    },
    handleError() {
      this.$message.error("上传失败");
    },
    handleExceed() {
      this.$message.warning = "只允许上传一个文件";
    },
    /**
     * 清空社区数据，有人认领的数据集不可以删除
     */
    removeAll() {
      this.$confirm("确定要清空吗?", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        removeAllCommunityDatasetApi(this.token)
          .then(() => {
            for (let i = 0; i < this.filterList.length; i++) {
              if (this.filterList[i].status == "无人认领") {
                this.filterList.splice(i, 1);
              }
            }
            for (let i = 0; i < this.list.length; i++) {
              if (this.list[i].status == "无人认领") {
                this.list.splice(i, 1);
              }
            }
          })
          .then(() => {
            this.$store.dispatch("myDataset/setMyDatasetList", this.list);
          });
      });
    },

    /**
     * 搜索数据集名字或描述
     */
    search() {
      let keywords = this.keywords.trim();

      if (this.searchTarget == "描述") {
        this.filterList = this.list.filter((item) =>
          item.description.includes(keywords)
        );
      } else {
        this.filterList = this.list.filter((item) =>
          item.name.includes(keywords)
        );
      }
    },

    /**
     * 领取标注任务，添加到个人数据集中
     */
    addToMyDataset(index) {
      // 设置数据集id
      addAnnotatedSetApi(this.filterList[index]);
      this.filterList[index].status = "有人认领"; // 更新数据集领取状态
      this.$message.success("领取成功，可以在个人数据集中查看~");
      内部;
    },

    /**
     * 编辑
     * @param {object} row 操作当前行数据
     */
    handleEdit(index, row) {
      this.showEditForm = true;
      this.listEditIndex = index;
      this.form.description = row.description;
      this.form.name = row.name;
      this.handleItemId = row.id;
    },

    /**
     * 更新数据
     */
    update() {
      this.filterList[this.listEditIndex].description = this.form.description;
      this.filterList[this.listEditIndex].name = this.form.name;
      updateCommunityDatasetInfoApi(this.filterList[this.listEditIndex]);
      this.list.forEach((item) => {
        if (item.id == this.handleItemId) {
          item.description = this.form.description;
          item.name = this.form.name;
        }
      });
      this.showEditForm = false;
    },

    /**
     * 删除数据集，有人认领的数据集不可以删除
     */
    handleDelete(index) {
      let id = this.filterList[index].id;
      deleteCommunityDatasetApi(id).then(() => {
        if (this.filterList[index].status == "无人认领") {
          this.filterList.splice(index, 1);
          for (let i = 0; i < this.list.length; i++) {
            if (this.list[i].id == id) {
              this.list.splice(i, 1);
              this.$store.dispatch("myDataset/setMyDatasetList", this.list);
              break;
            }
          }
        }
      });
    },

    /**
     * 表格样式
     */
    tableRowClassName({ row, rowIndex }) {
      row;
      if (rowIndex % 2) {
        return "even-row";
      }
      return "odd-row";
    },
  },
};
</script>
<style lang="scss">
// 按钮组
.button-group {
  width: 100%;
  display: inline;
  margin: 0 20px 20px 20px;
  &-item {
    margin-right: 20px;
    display: inline-block;
  }
}
// 清空按钮
.clear {
  float: right;
  margin-bottom: 20px;
}
// 搜索框
.search {
  margin-top: 20px;
  margin-bottom: 20px;
  .el-select {
    width: 150px;
  }
}
// 表格样式
.el-table .even-row {
  background: #daece9;
}
.el-table .odd-row {
  background: #f7faed;
}
// 单行显示文本
.single-line {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
