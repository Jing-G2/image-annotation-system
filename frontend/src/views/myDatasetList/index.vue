<template>
  <div class="app-container">
    <!-- 跳转到导入界面 -->
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
        <el-table-column label="操作" width="280" align="center">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="goToAnnotation(scope.$index, scope.row)"
            >
              标注
            </el-button>
            <el-button type="info" size="mini" vf @click="exportData(scope.row)"
              >导出</el-button
            >
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
      <output-options ref="outputOptions" />
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
import OutputOptions from "@/views/imageAnnotate/annotateContent/components/OutputOptions";

import {
  getMyDatasetInfoApi,
  deleteAnnotatedSetApi,
  removeAllAnnotatedSetApi,
  updateAnnotatedSetInfoApi,
} from "@/api/myDataset";
import { getToken } from "@/utils/auth";
import { mapGetters } from "vuex";

export default {
  name: "myDatasetTableList",
  components: {
    OutputOptions,
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        已标注: "success",
        未标注: "gray",
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
    ...mapGetters(["myDatasetList"]),
  },
  created() {
    // 获取个人数据集信息
    getMyDatasetInfoApi().then((res) => {
      // 顺序执行
      this.$store.dispatch("myDataset/setMyDatasetList", res.data.dataset_list);
      this.list = this.filterList = this.myDatasetList;
      this.listLoading = false;
    });
    // 括号外面类似异步执行
  },
  mounted() {
    this.list = this.filterList = this.myDatasetList;
    this.listLoading = false;
  },
  methods: {
    /**
     * 清空数据集
     */
    removeAll() {
      // TODO: 优化让只有无人领取的数据集被删除不可见，而有人领取的还可见
      this.$confirm("确定要删除吗?", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        removeAllAnnotatedSetApi(this.token).then((res) => {
          this.$store.dispatch("myDataset/setMyDatasetList", []);
          this.list = [];
          this.filterList = [];
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
     * 进行标注，跳转到标注页面
     */
    goToAnnotation(index) {
      //   要传参跳转
      this.$router.push(`/imageAnnotate/${this.filterList[index].id}`);
    },

    /**
     * : 数据集导出
     */
    exportData(row) {
      if (row.status == "未标注") {
        this.$message("当前数据集还未完成标注，请完成标注再导出~");
      } else {
        this.$refs.outputOptions.annotatedSet_id = row.id;
        this.$refs.outputOptions.fileName = row.name;
        this.$refs.outputOptions.dialogVisible = true;
      }
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
      updateAnnotatedSetInfoApi(this.filterList[this.listEditIndex]);
      this.list.forEach((item) => {
        if (item.id === this.handleItemId) {
          item.description = this.form.description;
          item.name = this.form.name;
        }
      });
      this.showEditForm = false;
    },

    /**
     * 删除数据集
     */
    handleDelete(index) {
      let id = this.filterList[index].id;
      deleteAnnotatedSetApi(id).then(() => {
        this.filterList.splice(index, 1);
        for (let i = 0; i < this.list.length; i++) {
          if (this.list[i].id == id) {
            this.list.splice(i, 1);
            this.$store.dispatch("myDataset/setMyDatasetList", this.list);
            break;
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
