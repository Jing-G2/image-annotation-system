<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card
          shadow="hover"
          class="mgb20"
          style="width: 400px; height: 400px"
        >
          <div class="user-info">
            <div class="el-upload">
              <el-upload
                class="avatar-uploader"
                :headers="{ 'annotate-system-token': token }"
                name="avatar"
                action="http://localhost:8000/api/setAvatar/"
                :show-file-list="false"
                accept="image/*"
                :on-success="handleSuccess"
                :on-error="handleError"
              >
                <img :src="avatar" class="avatar" alt="" />
              </el-upload>
              <p style="font-size: 10px">点击图片更换头像</p>
            </div>

            <div class="user-info-cont">
              <div class="user-info-name">
                {{ name }}
              </div>
            </div>
          </div>
          <div class="user-info-list">
            邮箱：
            <span>{{ email }}</span>
          </div>
          <div class="user-info-list">
            角色：
            <span>{{ roles[0] }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { getToken } from "@/utils/auth";
import TodoList from "./components/TodoList";
export default {
  name: "Dashboard",
  components: {
    TodoList,
  },
  computed: {
    token() {
      return getToken();
    },
    ...mapGetters(["name", "avatar", "roles", "email"]),
  },
  methods: {
    handleSuccess(response) {
      this.$store.dispatch("user/setAvatar", response.data.avatar);
    },
    handleError() {
      this.$message.error("上传失败");
    },
  },
};
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
}

.el-row {
  margin-bottom: 20px;
}

.avatar {
  width: 200px;
  height: 200px;
}

.user-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 3px solid #ccc;
  margin-bottom: 20px;

  &-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;

    div:first-child {
      font-size: 30px;
      color: #222;
    }
  }

  &-name {
    margin-left: -20px;
  }

  &-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;

    span {
      margin-left: 70px;
    }
  }

  .mgb20 {
    margin-bottom: 20px;
  }
}
</style>
